#!/usr/bin/python3
from fastapi import APIRouter,Request,Form,Response,Depends, HTTPException
from fastapi.responses import RedirectResponse,HTMLResponse
from hashlib import md5
import json,time,re,os

router = APIRouter()

async def ckadmin(request: Request):
    if 'admin' not in request['session']:
        raise HTTPException(status_code=403, detail="sysadmin invalid")

def ckurl(mo):
    if mo.group(0)[-4:].lower() in ('.jpg','.bmp','.png','jpeg','webp'):
        return '<img referrerpolicy="no-referrer" src="' + mo.group(0) + '" />'
    else:
        return '<a href="' + mo.group(0) + '">' + mo.group(0)[:40] + '</a>'

def hex_id(id):
    while True:
        rand = os.urandom(16)
        nt = time.time()
        hashable = "%s%s%s" % (rand, nt, id)
        hid = md5(hashable.encode("utf-8")).hexdigest()[8:23]
        if not os.path.exists('shudong/data/' + hid + '.json'):
            break
    return hid

@router.post("/add")
async def add(request: Request, text: str = Form(...)):

    text = re.sub('<[^<]+?>', '',text).replace('\r\n', '\r\n<br />')
    text = re.sub('(((ht|f)tps?:)?\/\/)([^\s]+)',ckurl,text,0,re.I)
    tm = int(time.time())
    
    fo = open("shudong/data/id.ini", "r+")
    id = int(fo.read())+1
    fo.seek(0)
    fo.write(str(id))
    fo.close()
    
    hid = hex_id(id)
    
    item={"id":id,'hid':hid,"time":tm,"status":0,"vote":0,"text":text}
    with open('shudong/data/' + str(id) + '.json', 'w') as f:
        json.dump(item, f, indent=4,ensure_ascii=False)
        os.symlink('./'+ str(id) + '.json','shudong/data/'+ str(hid) + '.json')
    
    #return RedirectResponse("/view/"+str(id),status_code=303)
    html = "<script language=\"javascript\" type=\"text/javascript\"> window.location.href=\"/view/" + hid + "\"; </script>"
    return HTMLResponse(content=html, status_code=200)
    
@router.post("/view/{hid}")
async def reply(request: Request,hid:str,text: str = Form(...)):
    filename = 'shudong/data/' + hid + '.json'
    if not os.path.exists(filename):
        return t.TemplateResponse("error.html", {"request": request, "title": '404! 哦豁'},status_code=404)
          
    text = re.sub('<[^<]+?>', '',text).replace('\r\n', '<br />\r\n')
    text = re.sub('(((ht|f)tps?:)?\/\/)([^\s]+)',ckurl,text,0,re.I)
    tm = int(time.time())

    item={"time":tm,"text":text}
    
    id = json.load(open(filename, 'r'))['id']
    
    if os.path.exists('shudong/data/r' + str(id) + '.json'):
        reps=json.load(open('shudong/data/r' + str(id) + '.json', 'r'))
    else:
        reps=[]
        
    reps.append(item)
    
    with open('shudong/data/r' + str(id) + '.json', 'w') as f:
        json.dump(reps, f, indent=4,ensure_ascii=False)           
    
    #return RedirectResponse("/view/"+str(id),status_code=303)
    html = "<script language=\"javascript\" type=\"text/javascript\"> window.location.href=\"/view/" + hid + "\"; </script>"
    return HTMLResponse(content=html, status_code=200)
    
@router.get("/vote/{hid}")
async def vote(hid:str,response: Response):
    filename = 'shudong/data/' + hid + '.json'
    if not os.path.exists(filename):
        response.status_code=404
    else:
        item=json.load(open(filename, 'r'))
        item['vote'] = int(item['vote']) + 1
        with open(filename, 'w') as f:
            json.dump(item, f, indent=4,ensure_ascii=False)
    return ""
        
@router.get("/delete/{id}",dependencies=[Depends(ckadmin)])
async def delete(id:int):
    filename = 'shudong/data/' + str(id) + '.json'
    if os.path.exists(filename):
        hid = json.load(open(filename, 'r'))['hid']
        os.remove('shudong/data/' + hid + '.json')
        os.remove('shudong/data/' + str(id) + '.json')
        if os.path.exists('shudong/data/r' + str(id) + '.json'):
            os.remove('shudong/data/r' + str(id) + '.json')
    return ""

@router.get("/hide/{id}",dependencies=[Depends(ckadmin)])
async def hide(id:int,response: Response):
    filename = 'shudong/data/' + str(id) + '.json'
    if not os.path.exists(filename):
        response.status_code=404
        return ""
    else:
        item=json.load(open(filename, 'r'))
        item['status'] = 4
        with open(filename, 'w') as f:
            json.dump(item, f, indent=4,ensure_ascii=False)
        return ""


@router.get("/r{id}/{rid}",dependencies=[Depends(ckadmin)])
async def delr(id:int,rid:int):
    
    if os.path.exists('shudong/data/r' + str(id) + '.json'):
        reps=json.load(open('shudong/data/r' + str(id) + '.json', 'r'))
        if len(reps) == 1:
            os.remove('shudong/data/r' + str(id) + '.json')
        else:
            del reps[rid]
            with open('shudong/data/r' + str(id) + '.json', 'w') as f:
                json.dump(reps, f, indent=4,ensure_ascii=False)
                
    return ""