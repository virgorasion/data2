var chart = AmCharts.makeChart("chartdiv", {
  "type": "serial",
  "theme": "none",
  "pathToImages": "https://www.amcharts.com/lib/3/images/",
  "dataProvider": [{
    "date": "2009-10-02",
    "value": 5
  }, {
    "date": "2009-10-03",
    "value": 15
  }, {
    "date": "2009-10-04",
    "value": 13
  }, {
    "date": "2009-10-05",
    "value": 17
  }, {
    "date": "2009-10-06",
    "value": 15
  }, {
    "date": "2009-10-09",
    "value": 19
  }, {
    "date": "2009-10-10",
    "value": 21
  }, {
    "date": "2009-10-11",
    "value": 20
  }, {
    "date": "2009-10-12",
    "value": 20
  }, {
    "date": "2009-10-13",
    "value": 19
  }, {
    "date": "2009-10-16",
    "value": 25
  }, {
    "date": "2009-10-17",
    "value": 24
  }, {
    "date": "2009-10-18",
    "value": 26
  }, {
    "date": "2009-10-19",
    "value": 27
  }, {
    "date": "2009-10-20",
    "value": 25
  }, {
    "date": "2009-10-23",
    "value": 29
  }, {
    "date": "2009-10-24",
    "value": 28
  }, {
    "date": "2009-10-25",
    "value": 30
  }, {
    "date": "2009-10-26",
    "value": 72,
    "customBullet": "https://www.amcharts.com/lib/3/images/redstar.png",
    "customDescription": "Hi there"
  }, {
    "date": "2009-10-27",
    "value": 43
  }, {
    "date": "2009-10-30",
    "value": 31
  }, {
    "date": "2009-11-01",
    "value": 30
  }, {
    "date": "2009-11-02",
    "value": 29
  }, {
    "date": "2009-11-03",
    "value": 27
  }, {
    "date": "2009-11-04",
    "value": 26
  }],
  "valueAxes": [{
    "axisAlpha": 0,
    "dashLength": 4,
    "position": "left"
  }],
  "graphs": [{
    "bulletSize": 14,
    "customBullet": "https://www.amcharts.com/lib/3/images/star.png",
    "customBulletField": "customBullet",
    "balloonText": "[[customDescription]]",
    "labelText": "[[customDescription]]",
    "valueField": "value"
  }],
  "marginTop": 20,
  "marginRight": 20,
  "marginLeft": 40,
  "marginBottom": 20,
  "chartCursor": {
    "graphBulletSize": 1.5
  },
  "autoMargins": false,
  "dataDateFormat": "YYYY-MM-DD",
  "categoryField": "date",
  "categoryAxis": {
    "parseDates": true,
    "axisAlpha": 0,
    "gridAlpha": 0,
    "inside": true,
    "tickLength": 0
  }
});