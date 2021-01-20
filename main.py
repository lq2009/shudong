#!/usr/bin/python3

from fastapi import FastAPI
from starlette.middleware.sessions import SessionMiddleware

from fastapi.responses import HTMLResponse
from fastapi.exceptions import RequestValidationError
from starlette.exceptions import HTTPException as StarletteHTTPException

from fastapi.templating import Jinja2Templates
from shudong.controller import user,action,page


app = FastAPI(openapi_url=None)
app.add_middleware(SessionMiddleware, secret_key='dta3dsf',max_age=25200,session_cookie='sd_sid')
t = Jinja2Templates(directory="shudong/view")

@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request, exc):
    return t.TemplateResponse("error.html",{"request": request, "title": '参数错误'},status_code=422)
    
@app.exception_handler(StarletteHTTPException)
async def http_exception_handler(request, exc):
    return t.TemplateResponse("error.html", {"request": request, "title": exc.detail},status_code=exc.status_code)#exc.status_code
    
#add|reply|  (vote|delete|hide|ban)/(.*)| r(\d+)/(\d+)
app.include_router(action.router)
#(kui) view/(\d*)
app.include_router(page.router)
