#!/usr/bin/python
#encoding=utf-8
'''
基于BaseHTTPServer的http server实现，包括get，post方法，get参数接收，post参数接收。
'''
import io,shutil  
#import getopt #,string
from os.path import join, abspath, dirname, exists
from os import walk
import os, sys
#multiThreading
import threading, time
import json
try:
    from BaseHTTPServer import HTTPServer, BaseHTTPRequestHandler
    from SocketServer import ThreadingMixIn
    import urllib
    #from urllib import quote as urlquote
except ImportError:
    from http.server import BaseHTTPRequestHandler,HTTPServer
    from socketserver import ThreadingMixIn
    import urllib.request as urllib
    #from urllib.request import quote as urlquote

#print('python version ', sys.version)
BASE_DIR = os.path.abspath(os.path.dirname(__file__))
sys.path.insert(0, BASE_DIR)
static_path = join(BASE_DIR, 'static')

class MyRequestHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        mpath,margs=urllib.splitquery(self.path) # ?分割
        self.do_action(mpath, margs)

    def do_POST(self):
        mpath,margs=urllib.splitquery(self.path)
        datas = self.rfile.read(int(self.headers['content-length']))
        if type(datas) == type(b'b'):
            datas = datas.decode('utf8')
        self.do_action(mpath, datas)

    def do_action(self, path, args):
        fileext = path[-5:]
        #print path,'==>', fileext
        if fileext.find('.') >=0: # 'staticfile':
            self.static_file(path)
            return
        if path[-1] == '/':
            self.outputtxt(jessyPage())
            return
        mpath, action = getaction(path)
        margs = transDicts(args)
        ## >> bottle
        if mpath == "msg":
            self.outputtxt( msg_chat(action, margs) )
            return
        
        if mpath == "tongji":  # +++++ 统计 handsontable 
            from tongji.tongji import calc
            self.outputtxt( calc.do_act(action, margs))
            return

        if mpath == 'quit':
            if sys.platform[0] == 'l':
                self.outputtxt(u'''<br><h2><font color="#FF0000">需要关闭服务器：<br>
                      请在终端按Ctrl+C。<br>按“返回”继续</font></h2>''')
            else:
                self.outputtxt(u'<br><h1><font color="#FF0000">服务器已关闭</font></h1>')
                stophttp()
        else:
            self.send_error(404, "File not found - Error URL")
        # <<<<<<<<<<<<<<<<<<<<<<<<<<<<<< bottle

    def static_file(self, path):
        path = decodeURI(path)
        real_path = os.path.join(static_path, path[1:])
        #print 'real_path == >',real_path
        try:
            if os.path.exists(real_path):
                f =open(real_path, 'rb')
                size = os.path.getsize(real_path)
                self.send_response(200)
                self.send_header("Content-type", getContentType(path))
                self.send_header("Content-length", size)
                self.end_headers()
                shutil.copyfileobj(f, self.wfile)
            else:
                self.send_error(404, "File not found - Error File")
        except Exception as err:
            print (str(err))
            self.send_error(404, "File not found - Error")

    def outputtxt(self, content):
        #指定返回编码
        enc = "UTF-8"
        content = content.encode(enc)          
        f = io.BytesIO()
        f.write(content)
        f.seek(0)  
        self.send_response(200)  
        self.send_header("Content-type", "text/html; charset=%s" % enc)  
        self.send_header("Content-Length", str(len(content)))  
        self.end_headers()  
        shutil.copyfileobj(f,self.wfile)

class ThreadedHTTPServer(ThreadingMixIn, HTTPServer):
    """Handle requests in a separate thread."""


# >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>> jessyink \\\
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
        act = form["act"] #from control
        print('say=>', form)
        msg = json.loads(form["msg"],encoding='utf-8')  #{'jessid':2,'jessyslide':[22,44]}
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
        act = form["msgid"] # id 1
        second = 0
        try:
            while True:
                if act in msg_txt:
                    msg = msg_txt[act]
                    print('{"returnjson":%s}' % msg)
                    return '{"returnjson":%s}' % msg
                else:
                    time.sleep(0.01)
                    second += 1
                    if second > 2000:  #100/second
                        return '{"returnjson":"hear none"}'
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
        page +=  '<p><a target="_blank" href="' + encodeURI(ritem) + '?jessid=' + str(jessid) + \
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
    return urllib.quote(url)

def decodeURI(url):
    return urllib.unquote(url)
# >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>> jessyink ///

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

def stophttp():
    print ("stop http server")
    global server
    server.socket.close()
    #server.shutdown()
    sys.exit()
    quit()

def starthttp():
    print ("start http server...")
    print ('BASE_DIR http=== >',BASE_DIR)
    try:
        global server
        #server = HTTPServer(('', 9981), MyRequestHandler)
        ip = get_ip()
        server = ThreadedHTTPServer((ip, 8080), MyRequestHandler)
        print ('started httpserver... \n http://%s:8080/'%ip)
        server.serve_forever()
    except KeyboardInterrupt:
        server.socket.close()

html_head = '<html>\n<head>\n<title>%(title)s</title>\n</head>\n<body>\n'
html_tail = '\n</body>\n</html>\n'
html_form = '''<form action="/yicuo/update" method="post"><input type="text" name="idd">
             <input type="text" name="ming"><input type="submit"></form>'''

mime_types ={
    '*'    :'application/octet-stream',
    '.html':'text/html ; charset=utf-8',
    '.htm' :'text/html ; charset=utf-8',
    '.css' :'text/css ; charset=utf-8',
    '.svg' :'image/svg+xml',
    '.ico' :'image/x-icon',
    '.js'  :'application/x-javascript; charset=utf-8',
    '.jpg' :'image/jpeg',
    '.png' :'image/png',
    '.txt' :'text/plain',
    '.gif' :'image/gif'
}

def getExtname(path):
    "得到扩展名"
    dot = path.rfind('.')
    if dot < 0 :
        return None
    return path[dot:]

def getContentType(path):
    "返回这个文件的Content-type的字符串"
    extname = getExtname(path)
    if extname in mime_types:
        return mime_types[extname]
    else:
        return mime_types['*']

def getaction(mpath):
    a = dopath = action = ''
    try:
        a, dopath, action = mpath.split('/')
    except:
        return 'staticfile', mpath
    return dopath, action

def transDicts(params):
    #print('params==>',params)
    dicts={}
    try:
        if len(params)==0:
            return
        params = params.split('&')
        for param in params:
            #print 'param == >', param
            equalindex = param.find('=')
            if equalindex > -1: 
                dicts[urllib.unquote(param[0:equalindex],encoding='utf8')] = \
                      urllib.unquote(param[equalindex+1:],encoding='utf8')
        #print('dicts==>',dicts)
        return dicts
    except:
        return {}


if __name__=='__main__':
    #import webbrowser
    #webbrowser.open("http://127.0.0.1:9981/index.html")
    starthttp()
    pass


'''
from BaseHTTPServer import HTTPServer, BaseHTTPRequestHandler
from SocketServer import ThreadingMixIn
import threading
import time

class Handler(BaseHTTPRequestHandler):

    def do_GET(self):
        self.send_response(200)
        self.end_headers()
        message =  threading.currentThread().getName()
        self.wfile.write(message)
        if (int(message[-1])%2 == 0):
            time.sleep(5)
        self.wfile.write("<h1>sssss</h1>")
        self.wfile.write('\n')
        return

class ThreadedHTTPServer(ThreadingMixIn, HTTPServer):
    """Handle requests in a separate thread."""

if __name__ == '__main__':
    server = ThreadedHTTPServer(('localhost', 8080), Handler)
    print 'Starting server, use <Ctrl-C> to stop'
    server.serve_forever()
'''