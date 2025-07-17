from fastapi import FastAPI, Request, Query
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import HTMLResponse, JSONResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
import logging

# Güvenlik modüllerini içe aktar
from modules.sql_injection import scan_sql_injection
from modules.xss import scan_xss
from modules.waf_detect import detect_waf
from modules.open_redirect import scan_open_redirect
from modules.cors_check import check_cors
from modules.ssl_check import check_ssl
from modules.tech_detect import detect_tech
from modules.clickjacking import check_clickjacking
from modules.csrf_check import check_csrf
from modules.lfi_rfi_check import check_lfi_rfi
from modules.directory_traversal import check_directory_traversal
from modules.admin_panel_finder import find_admin_panel
from modules.crlf_check import check_crlf_injection

# Uygulama tanımı
app = FastAPI(
    title="THT Güvenlik Taraması",
    description="Gerçek zamanlı web güvenlik açık tarayıcısı.",
    version="2.0.0"
)

# Loglama sistemi
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# CORS yapılandırması (gerekirse daha sınırlı yap)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # TODO: Prod ortamında belirli domain'lerle sınırla!
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Statik dosyalar ve şablonlar
app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="templates")


@app.get("/", response_class=HTMLResponse)
async def root(request: Request):
    """
    Ana HTML arayüzü döndürülür.
    """
    return templates.TemplateResponse("index.html", {"request": request})


@app.get("/api/vulnscan", response_class=JSONResponse)
async def vuln_scan(url: str = Query(..., description="Taranacak hedef URL")):
    """
    Hedef URL üzerinde tüm güvenlik açıklarını tarar.
    """
    logger.info(f"Taramaya başlandı: {url}")

    try:
        results = {
            "sql_injection": scan_sql_injection(url),
            "xss": scan_xss(url),
            "waf": detect_waf(url),
            "open_redirect": scan_open_redirect(url),
            "cors": check_cors(url),
            "ssl": check_ssl(url),
            "tech": detect_tech(url),
            "clickjacking": check_clickjacking(url),
            "csrf": check_csrf(url),
            "lfi_rfi": check_lfi_rfi(url),
            "directory_traversal": check_directory_traversal(url),
            "admin_panel": find_admin_panel(url),
            "crlf": check_crlf_injection(url),
            
        }

        logger.info(f"Tarama tamamlandı: {url}")
        return results

    except Exception as e:
        logger.error(f"Hata oluştu: {e}")
        return JSONResponse(status_code=500, content={"status": "error", "message": str(e)})
