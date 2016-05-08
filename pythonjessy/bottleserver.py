#!/usr/bin/env python3
# coding: utf-8

from bottle import route, run
from bottle import static_file, request, response #get, post,
from os.path import join, abspath, dirname
import sys
BASE_DIR = abspath(dirname(__file__))
#BASE_DIR = abspath('')
sys.path.insert(0, BASE_DIR)

static_path = join(BASE_DIR, 'static')
@route('/')
@route('')
def server_default():
    return static_file("b-index.html", root=BASE_DIR)

@route('<filepath:re:.+\..+>')  #URI带点的
def server_static_file(filepath):
    print('filepath root ==>',filepath)
    return static_file(filepath, root=BASE_DIR)

# <<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<
## myserver main
import tiku
yicuoti = tiku.c_tiku('myc', u'《易错题库》')
mingyanti = tiku.c_tiku('mmy', u'《名言题库》')
zhkaoti = tiku.c_tiku('mzk-in', u'《中考备考题库》')
TIKU = {'yicuo':yicuoti, 'mingyan':mingyanti, 'zhkao':zhkaoti }
# <<<<<<< myserver
@route('/<whichmod>/<action>', method='GET')
def md_select_get(whichmod, action):
    return to_module(whichmod, action, request.query)

@route('/<whichmod>/<action>', method='POST')
def md_select_post(whichmod, action):
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
#    if whichmod == "yicuo":   # +++++ 初一初二易错题
#        return yicuoti.do_act(action, form)
#    if whichmod == "mingyan": # +++++ 名言题库
#        return mingyanti.do_act(action, form)
#    if whichmod == "zhkaoti": # +++++ 中考备考题库
#        return zhkaoti.do_act(action, form)
#    else:
#        return

# >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>

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

run(host='', port=8080, debug=True, reloader=True)  #debug
#run(server='rocket', host='localhost', port=8080, debug=True, reloader=True) # Multithreading
