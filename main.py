
from fastapi import FastAPI, Request
from fastapi.staticfiles import StaticFiles
from fastapi.responses import JSONResponse
from starlette.templating import Jinja2Templates
import uvicorn

from modules.sql_injection import scan_sql_injection
from modules.xss import scan_xss
from modules.waf_detect import detect_waf
from modules.open_redirect import check_open_redirect
from modules.cors_check import check_cors
from modules.ssl_check import check_ssl
from modules.tech_detect import detect_tech
from modules.clickjacking import check_clickjacking

app = FastAPI()
app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="templates")

@app.get("/")
async def home(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

@app.get("/scan")
async def scan(url: str):
    try:
        return {
            "sql_injection": scan_sql_injection(url),
            "xss": scan_xss(url),
            "waf": detect_waf(url),
            "open_redirect": check_open_redirect(url),
            "cors": check_cors(url),
            "ssl": check_ssl(url),
            "tech": detect_tech(url),
            "clickjacking": check_clickjacking(url)
        }
    except Exception as e:
        return JSONResponse(content={"status": "error", "message": str(e)}, status_code=500)

if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8000)
