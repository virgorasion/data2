var http = require("http");
var express = require('express');
var app = express();
var mysql      = require('mysql');
var bodyParser = require('body-parser');

var connection = mysql.createConnection({
  host     : 'localhost',
  user     : 'root',
  password : 'papangjou',
  database : 'gotest'
});

connection.connect(function(err) {
  if (err) throw err
  console.log('You are now connected...')
})


app.use( bodyParser.json() );       // to support JSON-encoded bodies
app.use(bodyParser.urlencoded({     // to support URL-encoded bodies
  extended: true
}));

var server = app.listen(3000, "127.0.0.1", function () {
 
    var host = server.address().address
    var port = server.address().port

    console.log("Example app listening at http://%s:%s", host, port)
   
});

//rest api to get all results
app.get('/', function (req, res) {
    console.log(req);
    connection.query('select * from person', function (error, results, fields) {
        if (error) throw error;
        res.end(JSON.stringify(results));
    });
});