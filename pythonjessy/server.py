#!/usr/bin/env python3
#coding:utf-8

from bottle import route, run
from bottle import static_file, request, response #get, post,
from os.path import join, abspath, dirname
from os import walk
import sys
import json
try:
    from urllib.request import quote as urlquote
except ImportError:
    from urllib import quote as urlquote
#json.dumps(mydata)  dict => str | json.loads(jsondata) str => dict
BASE_DIR = abspath(dirname(__file__))
#BASE_DIR = abspath('')
sys.path.insert(0, BASE_DIR)

def formget(form, name):
    getstr = ""
    try:
        getstr = form.getunicode(name) #bottle
    except:
        getstr = form.get(name)
    return getstr

static_path = join(BASE_DIR, 'static')
@route('/')
@route('')
def server_default():
    return jessyPage() #static_file("b-index.html", root=BASE_DIR)

@route('<filepath:re:.+\..+>')  #URI带点的
def server_static_file(filepath):
    print('filepath root ==>',filepath)
    #return static_file(filepath, root=BASE_DIR)
    return static_file(filepath, root=static_path)

# <<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<
## myserver main
#ljj#import tiku
#ljj#yicuoti = tiku.c_tiku('myc', u'《易错题库》')
#ljj#mingyanti = tiku.c_tiku('mmy', u'《名言题库》')
#ljj#zhkaoti = tiku.c_tiku('mzk-in', u'《中考备考题库》')
#ljj#TIKU = {'yicuo':yicuoti, 'mingyan':mingyanti, 'zhkao':zhkaoti }
# <<<<<<< myserver
@route('/<whichmod>/<action>', method='GET')
def md_select_get(whichmod, action):
    return to_module(whichmod, action, request.query)

@route('/<whichmod>/<action>', method='POST')
def md_select_post(whichmod, action):
    if whichmod == "msg":
        return msg_chat(action, request.forms)
    return to_module(whichmod, action, request.forms)

def to_module(whichmod, action, form):
    ## myserver main
    if whichmod == "tongji":  # +++++ 统计 handsontable 
        from tongji.tongji import calc
        tongji_path = join(BASE_DIR, 'tongji')
        return calc.do_act(action, form)
    elif whichmod in TIKU:
        return TIKU[whichmod].do_act(action, form)
    else:
        return

# >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
msg_txt = {} #   "{"act":"from control", "msg":"{'jessid':2,'jessyslide':[22,44]}"}"
msg_id = 0
def msg_chat(action, form):
    global msg_id
    global msg_txt
    if action == "connect":
        curid = msg_id
        if curid == 0:
            curid = 1
        return '{"returnjson":%s}' % msg_id
    if action == "say":
        act = formget(form,"act") #from control
        msg = json.loads(formget(form,"msg"))  #{'jessid':2,'jessyslide':[22,44]}
        #msg = formget(form,"msg")
        #msg.replace('"', "'")
        msg_id = msg_id + 1
        try:
            msg_txt.pop(str(msg_id-100))
        except Exception as e:
            pass
        msg["act"] = act
        msg_txt[str(msg_id)] = json.dumps(msg)
        print(msg)
        return '{"returnjson":"say ok"}'
    if action == "hear":
        act = formget(form, "msgid") # id 1
        try:
            msg = msg_txt[act]
            print('{"returnjson":%s}' % msg)
            return '{"returnjson":%s}' % msg
        except Exception as e:
            #print(str(e))
            return '{"returnjson":"hear none"}'

def jessyPage():
    global static_path
    page = '<html><head><meta charset="utf-8" /><title>Python JessyInk</title></head><body>'
    fileList = []
    for root, dirs, files in walk(static_path, False, followlinks=True):
        for name in files:
            if name.endswith('index.html') or name.endswith('index.htm'):
                fileList.append(join(root,name))
    jessid = 0
    for name in fileList:
        jessid += 1
        ritem = name.replace(static_path, '')
        ritem = ritem.replace('\\', '/')
        poss = GetUrlFileName(ritem)
        page +=  '<p><a target="_blank" href="' + ritem + '?jessid=' + str(jessid) + \
                    '&name=' + encodeURI(poss) +'">' + ritem + '</a>'

        page +=  '&nbsp;&nbsp;<a target="_blank" href="/control.html?jessid=' + str(jessid) + \
                    '&name=' + encodeURI(poss) + '"> __Control__ </a></p>'
    page += '</body></html>'
    return page

def GetUrlFileName(url):
    try:
        i=url.index('/')
        fn = url.split('/')
    except:
        fn = url.split('\\')
    fn = fn[-1]
    fn = fn.replace("index.html","");
    fn = fn.replace("index.htm","");
    return fn

def encodeURI(url):
    return urlquote(url)

# +++++++ 上传 ++++++++++++++++++++++++++++++++++++++++++####
@route('/upload', method='POST')
def do_upload():
    category   = request.forms.get('Path')
    upload     = request.files.get('upload')
    if category:
        save_path = category
    else:
        save_path = join(BASE_DIR, 'upload')
    if upload:
        #name, ext = os.path.splitext(upload.filename)
        #if ext not in ('.png','.jpg','.jpeg'):
        #    return 'File extension not allowed.'
        save_path = join(save_path, upload.raw_filename)
        try:
            #print((save_path, dir(upload.file), dir(upload.save)))
            upload.save(save_path) # appends upload.filename automatically
            okk = "<br>OK<br>" 
        except Exception as e:
            okk = str(e)
            upload.file.close
    return form_upload() + okk

@route('/upload', method='GET')
def form_upload():
    upform = '''<html><head><meta charset="utf-8" /><title>File Upload</title><body>
    <form action="/upload" method="post" enctype="multipart/form-data">
    Path:      <input type="text" name="Path" />
    Select a file: <input type="file" name="upload" />
    <input type="submit" value="Start upload" />
    </form></body><html>'''
    return upform

# ======= 上传  ==========================================####

import socket
def get_ip():
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    try:
        # doesn't even have to be reachable
        s.connect(('10.255.255.255', 0))
        IP = s.getsockname()[0]
    except:
        IP = '127.0.0.1'
    finally:
        s.close()
    return IP

run(host=get_ip(), port=8080, debug=True, reloader=True)  #debug
#run(server='rocket', host='localhost', port=8080, debug=True, reloader=True) # Multithreading

'''

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
      //console.log(dev);
      if (dev.indexOf('wlan') > -1 || dev.indexOf('eth') > -1) {
          ifaces[dev].forEach(function(details){  
              if (details.family=='IPv4') {  
                 console.log(dev+':'+details.address);  
                 ipmap = details.address;
              }
          });
          return ipmap;
      }
    }
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
  //console.log('a user connected');
  //socket.id

  socket.on('disconnect', function(){
    //console.log('user disconnected');
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
'''
