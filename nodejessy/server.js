var workpath = '';
//'/1509';
var serverport = 8001;
var staticfolder ='/public';

console.log('__dirname' + ":" + __dirname);

var os=require('os');
function getLocalIP() {
    var ifaces=os.networkInterfaces();
    var ipmap = '127.0.0.1';
    for (var dev in ifaces) {  
      if (dev.indexOf('wlan0') != -1) {
      
      ifaces[dev].forEach(function(details){  
        if (details.family=='IPv4') {  
          console.log(dev+':'+details.address);  
          ipmap = details.address;
          }  
       });  
      }
    }
    return ipmap;
}

var LocalIP = getLocalIP();

var fs = require('fs'),
  fileList = [];
 
function deep_walk(path){
  var dirList = fs.readdirSync(path);
  dirList.forEach(function(item){
    if(fs.statSync(path + '/' + item).isDirectory()){
      walk(path + '/' + item);
    }else{
      fileList.push(path + '/' + item);
    }
  });
}
 
function walk(path){
  var dirList = fs.readdirSync(path);
 
  dirList.forEach(function(item){
    filename = path + '/' + item;
    if(fs.statSync(filename).isFile()){
      if (filename.toLocaleLowerCase().lastIndexOf('index.htm') > 1){
        fileList.push(filename);
      }
    }
  });
 
  dirList.forEach(function(item){
    if(fs.statSync(path + '/' + item).isDirectory()){
      walk(path + '/' + item);
    }
  });
}

function GetUrlFileName(url) {
    var fn = url.split('\/');
    fn = fn[fn.length - 1];
    fn = fn.replace("index.html","");
    fn = fn.replace("index.htm","");
    return fn;
}

var express = require('express')
    , app = express()
    , server = require('http').createServer(app)
    , io = require('socket.io').listen(server);

app.use(express.static(__dirname + staticfolder));

app.get('/', function (req, res) {
    res.set('Content-Type', 'text/html');
    fileList = [];
    walk(__dirname + staticfolder + workpath);
    var jessid = serverport;
    var ressend = '<html><head><title>Node JessyInk</title></head><body>';
    fileList.forEach(function(item){
        jessid += 1;
        ritem = item.replace((__dirname +staticfolder), ('http://' + LocalIP + ':' + serverport));
        poss = GetUrlFileName(ritem);
        ressend +=  '<p><a target="_blank" href="' + ritem + '?jessid=' + jessid + 
                    '&name=' + encodeURI(poss) +'">' + ritem + '</a>';

        ressend +=  '&nbsp;&nbsp;<a target="_blank" href="/control.html?jessid=' + jessid + 
                    '&name=' + encodeURI(poss) + '"> __Control__ </a></p>';
    });
    res.send(ressend+'</body></html>');
    //console.log(fileList);
    //res.sendfile(__dirname + '/index.html');
});

//app.get('/assets/*', function (req, res) {
//    res.sendfile(__dirname + req.originalUrl);
//    //console.log(req);
//    });

io.on('connection', function(socket){
  console.log('a user connected');
  //socket.id

  socket.on('disconnect', function(){
    console.log('user disconnected');
  });
    
  socket.on('chat message', function(msg){
    console.log('message: ' + socket.conn.remoteAddress + ': ' + msg);
 
    io.emit('chat message', socket.conn.remoteAddress + ': ' + msg);
  });

//  -------- jessyInk  Begin -------
  socket.on('from control', function(msg){
    //console.log('from control: ' + msg);
    io.emit('from control', msg);
  });
  
  socket.on('from jessy', function(msg){
    //console.log('from jessy: ' + msg);
    io.emit('from jessy', msg);
  });
//  -------- jessyInk  End -------
});



server.listen(serverport, function() {
  console.log('start at port: http://' + LocalIP + ':' + server.address().port);
});
