from fastapi import FastAPI, Request, Query
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates

from modules.sql_injection import scan_sql_injection
from modules.xss import scan_xss
from modules.waf_detect import detect_waf
from modules.open_redirect import scan_open_redirect
from modules.cors_check import check_cors
from modules.ssl_check import check_ssl
from modules.tech_detect import detect_tech
from modules.clickjacking import check_clickjacking

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="templates")

@app.get("/", response_class=HTMLResponse)
async def root(request: Request):
    return templates.TemplateResponse("advanced.html", {"request": request})

@app.get("/api/vulnscan")
async def vuln_scan(url: str = Query(...)):
    return {
        "sql_injection": scan_sql_injection(url),
        "xss": scan_xss(url),
        "waf": detect_waf(url),
        "open_redirect": scan_open_redirect(url),
        "cors": check_cors(url),
        "ssl": check_ssl(url),
        "tech": detect_tech(url),
        "clickjacking": check_clickjacking(url),
    }
