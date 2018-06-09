# encoding: utf-8

from pylons import cache
import sqlalchemy.exc

import ckan.logic as logic
import ckan.lib.search as search
import ckan.lib.base as base
import ckan.model as model
import ckan.lib.helpers as h

import ckan.plugins.toolkit as toolkit

# from ckan.common import _, config, c

from ckan.common import _, c, request, response
import ckan.plugins as p

CACHE_PARAMETERS = ['__cache', '__no_cache__']


class HomeController(base.BaseController):
    # def __init__(self, error=None):
        # Do any plugin login stuff
        # for item in p.PluginImplementations(p.IAuthenticator):
        #     item.login()
        #
        # if 'error' in request.params:
        #     h.flash_error(request.params['error'])
        #
        # if not c.user:
        #     came_from = request.params.get('came_from')
        #     if not came_from:
        #         came_from = h.url_for(controller='user', action='logged_in')
        #     c.login_handler = h.url_for(
        #         self._get_repoze_handler('login_handler_path'),
        #         came_from=came_from)
        #     if error:
        #         vars = {'error_summary': {'': error}}
        #     else:
        #         vars = {}
        #     h.redirect_to(controller='user', action='login')

    repo = model.repo

    def __before__(self, action, **env):
        try:
            base.BaseController.__before__(self, action, **env)
            context = {'model': model, 'user': c.user,
                       'auth_user_obj': c.userobj}
            logic.check_access('site_read', context)
        except logic.NotAuthorized:
            base.abort(403, _('Not authorized to see this page'))
        except (sqlalchemy.exc.ProgrammingError,
                sqlalchemy.exc.OperationalError), e:
            # postgres and sqlite errors for missing tables
            msg = str(e)
            if ('relation' in msg and 'does not exist' in msg) or \
                    ('no such table' in msg):
                # table missing, major database problem
                base.abort(503, _('This site is currently off-line. Database '
                                  'is not initialised.'))
                # TODO: send an email to the admin person (#1285)
            else:
                raise

    def _get_repoze_handler(self, handler_name):
        '''Returns the URL that repoze.who will respond to and perform a
        login or logout.'''
        return getattr(request.environ['repoze.who.plugins']['friendlyform'],
                       handler_name)

    def index(self, error=None,offset=0):
        for item in p.PluginImplementations(p.IAuthenticator):
            item.login()

        if 'error' in request.params:
            h.flash_error(request.params['error'])

        if not c.user:
            came_from = request.params.get('came_from')
            if not came_from:
                came_from = h.url_for(controller='user', action='logged_in')
            c.login_handler = h.url_for(
                self._get_repoze_handler('login_handler_path'),
                came_from=came_from)
            if error:
                vars = {'error_summary': {'': error}}
            else:
                vars = {}
            h.redirect_to(controller='user', action='login')
            # return base.render('user/login.html', extra_vars=vars)
        else:
            try:
                # package search
                context = {'model': model, 'session': model.Session,
                           'user': c.user, 'auth_user_obj': c.userobj,
                           'for_view': True}
                data_dict = {
                    'q': '*:*',
                    'facet.field': h.facets(),
                    'rows': 4,
                    'start': 0,
                    'sort': 'views_recent desc',
                    'fq': 'capacity:"public"'
                }
                query = logic.get_action('package_search')(
                    context, data_dict)
                c.search_facets = query['search_facets']
                c.package_count = query['count']
                c.datasets = query['results']

                c.facet_titles = {
                    'organization': _('Organizations'),
                    'groups': _('Groups'),
                    'tags': _('Tags'),
                    'res_format': _('Formats'),
                    'license': _('Licenses'),
                }

            except search.SearchError:
                c.package_count = 0

            if c.userobj and not c.userobj.email:
                url = h.url_for(controller='user', action='edit')
                msg = _('Please <a href="%s">update your profile</a>'
                        ' and add your email address. ') % url + \
                    _('%s uses your email address'
                        ' if you need to reset your password.') \
                    % config.get('ckan.site_title')
                h.flash_notice(msg, allow_html=True)

            q = request.params.get('q', u'')
            filter_type = request.params.get('type', u'')
            filter_id = request.params.get('name', u'')

            c.followee_list = logic.get_action('followee_list')(
                context, {'id': c.userobj.id, 'q': q})
            # c.dashboard_activity_stream_context = self._get_dashboard_context(
            #     filter_type, filter_id, q)
            c.dashboard_activity_stream = h.dashboard_activity_stream(
                c.userobj.id, filter_type, filter_id, offset
            )

            return base.render('home/index.html', cache_force=True)

    # def index(self, error=None):
    #     for item in p.PluginImplementations(p.IAuthenticator):
    #         item.login()
    #
    #     if 'error' in request.params:
    #         h.flash_error(request.params['error'])
    #
    #     if not c.user:
    #         came_from = request.params.get('came_from')
    #         if not came_from:
    #             came_from = h.url_for(controller='user', action='logged_in')
    #         c.login_handler = h.url_for(
    #             self._get_repoze_handler('login_handler_path'),
    #             came_from=came_from)
    #         if error:
    #             vars = {'error_summary': {'': error}}
    #         else:
    #             vars = {}
    #         h.redirect_to(controller='user', action='login')
    #     else:
    #         try:
    #             # package search
    #             context = {'model': model, 'session': model.Session,
    #                        'user': c.user, 'auth_user_obj': c.userobj}
    #             data_dict = {
    #                 'q': '*:*',
    #                 'facet.field': h.facets(),
    #                 'rows': 4,
    #                 'start': 0,
    #                 'sort': 'views_recent desc',
    #                 'fq': 'capacity:"public"'
    #             }
    #             query = logic.get_action('package_search')(
    #                 context, data_dict)
    #             c.search_facets = query['search_facets']
    #             c.package_count = query['count']
    #             c.datasets = query['results']
    #
    #             c.facet_titles = {
    #                 'organization': _('Organizations'),
    #                 'groups': _('Groups'),
    #                 'tags': _('Tags'),
    #                 'res_format': _('Formats'),
    #                 'license': _('Licenses'),
    #             }
    #
    #         except search.SearchError:
    #             c.package_count = 0
    #
    #         if c.userobj and not c.userobj.email:
    #             url = h.url_for(controller='user', action='edit')
    #             msg = _('Please <a href="%s">update your profile</a>'
    #                     ' and add your email address. ') % url + \
    #                 _('%s uses your email address'
    #                     ' if you need to reset your password.') \
    #                 % config.get('ckan.site_title')
    #             h.flash_notice(msg, allow_html=True)
    #
    #         return base.render('home/index.html', cache_force=True)

    def license(self):
        return base.render('home/license.html')

    def about(self):
        return base.render('home/about.html')

    def data_request(self):
	return toolkit.redirect_to('https://docs.google.com/forms/d/e/1FAIpQLSfvptqN_XbvbxJlNEc-GFK1hOxm_It2Zf_Wvb2ggzyJ0Ja8-w/viewform')

    def cache(self, id):
        '''Manual way to clear the caches'''
        if id == 'clear':
            wui_caches = ['stats']
            for cache_name in wui_caches:
                cache_ = cache.get_cache(cache_name, type='dbm')
                cache_.clear()
            return 'Cleared caches: %s' % ', '.join(wui_caches)

    def cors_options(self, url=None):
        # just return 200 OK and empty data
        return ''
