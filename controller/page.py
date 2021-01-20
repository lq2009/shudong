#!/usr/bin/python3
from fastapi import APIRouter,Request
from fastapi.templating import Jinja2Templates
from fastapi.responses import RedirectResponse,HTMLResponse
import json,time,re,os,random

t = Jinja2Templates(directory="shudong/view")

router = APIRouter()

@router.get("/")
async def index(request: Request):
    fo = open("shudong/data/id.ini", "r")
    id = int(fo.read())
    fo.close()
    
    items=[]
    while True:
        filename = 'shudong/data/' + str(id) + '.json'
        id-=1
        if os.path.exists(filename):
            item=json.load(open(filename, 'r'))
            item['text']=''.join(item['text'].splitlines()[:7])
            item['time']=time.strftime("%Y-%m-%d %H:%M +", time.localtime(int(item['time'])))
            items.append(item)
            
        if len(items)==12:
            break
    return t.TemplateResponse("index.html",{"request": request,'items':items,'page':'index'})

@router.get("/view/{hid}")
async def view(request: Request,hid:str):
    filename = 'shudong/data/' + hid + '.json'
    if not os.path.exists(filename):
        return t.TemplateResponse("error.html", {"request": request, "title": '404! 哦豁'},status_code=404)
    
    item=json.load(open(filename, 'r'))
    if(hid != item['hid']):
        return t.TemplateResponse("error.html", {"request": request, "title": '404! 哦豁'},status_code=404)
    item['title']=re.sub('<[^<]+?>', '', item['text']).replace('\r\n', '').strip()[:35]
    item['time']=time.strftime("%Y-%m-%d %H:%M+", time.localtime(int(item['time'])))
    
    rfilename = 'shudong/data/r' + str(item['id']) + '.json'
    if os.path.exists(rfilename):
        reps=json.load(open(rfilename, 'r'))
        for rep in reps:
            rep['index']=str(reps.index(rep))
            rep['time']=time.strftime("%Y-%m-%d %H:%M+", time.localtime(int(rep['time'])))
        cnum = len(reps)
    else:
        cnum = 0
        reps = None
    
    items=[]
    id = item['id']
    while True:
        id -= 1
        lfilename = 'shudong/data/' + str(id) + '.json'
        if os.path.exists(lfilename):
            litem=json.load(open(lfilename, 'r'))
            litem['text']=re.sub('<[^<]+?>', '', litem['text']).replace('\r\n', '').strip()[:70]
            items.append(litem)
            
        if len(items)==5 or id < 2:
            break
    
    return t.TemplateResponse("view.html",{"request": request,'item':item,'reps':reps,"cnum":cnum,'items':items})
    
@router.get("/post")
async def post(request: Request):
    return t.TemplateResponse("post.html", {"request": request})

@router.get("/kui")
async def kui():
    fo = open("shudong/data/id.ini", "r")
    id = random.randint(2,int(fo.read())-200)
    fo.close()
    
    while True:
        if os.path.exists('shudong/data/' + str(id) + '.json'):
            hid = json.load(open('shudong/data/' + str(id) + '.json', 'r'))['hid']
            #return RedirectResponse("/view/"+str(id))
            html = "<script language=\"javascript\" type=\"text/javascript\"> window.location.href=\"/view/" + hid + "\"; </script>"
            return HTMLResponse(content=html, status_code=200)
        id += 1