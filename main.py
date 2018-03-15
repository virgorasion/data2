import ckanclient
import re
import urllib, json
from ckanapi import RemoteCKAN

ckan = ckanclient.CkanClient(api_key="b39e64f6-50ab-4225-ac3c-3edc699d6e5c", base_location="http://localhost/api/")
mysite = RemoteCKAN('http://localhost/', apikey='b39e64f6-50ab-4225-ac3c-3edc699d6e5c')

for i in range(0,1000,40):
    nama = 'databoks'+str(i)
    print nama
    link = 'http://localhost/dataset/databoks'+str(i)
    print link
    
    dataset_entity = {
      'name': nama,
      'url': link,
    #   'download_url': 'https://cms.katadata.co.id/data/exportXls/2539?json=true&nama_data=indeks-tendensi-bisnis',
      # 'download_url': 'https://cms.katadata.co.id/data/exportXls/119847?json=true&nama_data=volume-impor-beras',
      # 'tags': 'my_dataset_keywords',
    #   'organizations': 'databok123',
      # 'notes': 'my_dataset_long_description',
    }

    ckan.package_register_post(dataset_entity)

    url = "https://cms.katadata.co.id/data/searchdata/-/-/-/-/-/-/-/-/"+str(i)+"?json=true"
    response = urllib.urlopen(url)
    data = json.loads(response.read())

    for i in range(40):
        # print data[str(i)]["link"]
        namadata=re.findall(r'nama_data=(\S+)', data[str(i)]["link"])
        # namaakhir=' '.join(namadata)
        namaakhir = re.sub(r"\-", " ", namadata[0])
        print namaakhir
    #   ckan.add_package_resource(nama, data[str(i)]["link"], resource_type='data',name=namaakhir, format='csv')
        mysite.action.resource_create(
            package_id=nama,
            url=data[str(i)]["link"],
            name=namaakhir,
            format='csv'
            # upload=open('/path/to/file/to/upload.csv', 'rb')
        )