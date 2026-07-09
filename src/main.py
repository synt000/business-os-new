from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.openapi.docs import get_swagger_ui_html
from fastapi.responses import HTMLResponse

from core.config import settings
from core.middlewares import SecurityInfrastructureMiddleware, setup_global_exception_handlers
from src.product.router import router as product_router

app = FastAPI(
    title="Business OS - မြန်မာလုပ်ငန်းသုံး စနစ်တော်ကြီး",
    version="5.0.0-Enterprise",
    docs_url=None,
    redoc_url=None,
    openapi_url="/api/v4/openapi.json"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
app.add_middleware(SecurityInfrastructureMiddleware)

setup_global_exception_handlers(app)
app.include_router(product_router)

@app.get("/api/v4/docs", include_in_schema=False)
async def custom_swagger_ui_portal_ingress():
    html_content = get_swagger_ui_html(
        openapi_url=app.openapi_url,
        title="Business OS - လုပ်ငန်းသုံး APIs ပေါ်တယ်လ်",
        swagger_css_url="https://jsdelivr.net"
    ).body.decode("utf-8")
    
    translated_html = html_content.replace(
        "</body>",
        """
        <script>
        window.addEventListener('load', function() {
            setInterval(function() {
                // ၁။ Group Headers ပြန်ဆိုခြင်း
                document.querySelectorAll('.opblock-tag span').forEach(el => {
                    if(el.innerText.includes('Authentication') || el.innerText.includes('auth') || el.innerText.includes('Engine')) el.innerText = '🔐 (၁) အကောင့်ဝင်ခြင်းနှင့် လုံခြုံရေး ဂိတ်ဝေး';
                    if(el.innerText.includes('Omnichannel') || el.innerText.includes('business')) el.innerText = '📦 (၂) ဆိုင်ခွဲ၊ POS အရောင်းနှင့် စာရင်းကိုင် လုပ်ငန်းသုံး အင်ဂျင်';
                });
                
                // ၂။ ခလုတ်များ ပြန်ဆိုခြင်း
                document.querySelectorAll('.authorize span').forEach(el => {
                    if(el.innerText === 'Authorize') el.innerText = 'သော့ခတ်မည် 🔓';
                });
                document.querySelectorAll('.btn.try-out__btn').forEach(el => {
                    el.innerText = 'လက်တွေ့စမ်းသပ်မည်';
                });
                document.querySelectorAll('.btn.execute').forEach(el => {
                    el.innerText = 'စနစ်မောင်းနှင်မည် (Execute)';
                });
                
                // ၃။ ဒုတိယ SCREEN: SCHEMAS စာသားများ မြန်မာပြန်ဆိုခြင်း Matrix
                document.querySelectorAll('.model-box-control span, h4 span').forEach(el => {
                    if(el.innerText === 'Schemas') el.innerText = '📋 ဒေတာ ပုံစံငယ်များ (Schemas)';
                    if(el.innerText === 'Model') el.innerText = 'ဒေတာ ဖွဲ့စည်းပုံ';
                });
                
                // ၄။ Schema Names များအား အမြင်ရှင်းအောင် မြန်မာလို Tag တွဲပေးခြင်း
                document.querySelectorAll('.model-title').forEach(el => {
                    if(el.innerText === 'BranchCreateInboundSchema') el.innerText = '🏢 BranchCreateInboundSchema (ဆိုင်ခွဲအသစ်ဆောက်ရန် ဒေတာပုံစံ)';
                    if(el.innerText === 'CategoryCreateInboundSchema') el.innerText = '🗂️ CategoryCreateInboundSchema (အုပ်စုခွဲအသစ်ဆောက်ရန် ဒေတာပုံစံ)';
                    if(el.innerText === 'CustomerCreateInboundSchema') el.innerText = '👥 CustomerCreateInboundSchema (CRM ဖောက်သည်သစ်ထည့်ရန် ဒေတာပုံစံ)';
                    if(el.innerText === 'OrderCreateInboundSchema') el.innerText = '🛒 OrderCreateInboundSchema (POS အမှာစာအရောင်းသွင်းရန် ဒေတာပုံစံ)';
                    if(el.innerText === 'ProcurementCreateInboundSchema') el.innerText = '📦 ProcurementCreateInboundSchema (ကုန်ပစ္စည်းအဝယ်စာရင်းသွင်းရန် ဒေတာပုံစံ)';
                    if(el.innerText === 'ProductCreateInboundSchema') el.innerText = '🏷️ ProductCreateInboundSchema (ကုန်ပစ္စည်းအသစ်တင်ရန် ဒေတာပုံစံ)';
                    if(el.innerText === 'WorkspaceInviteInboundSchema') el.innerText = '✉️ WorkspaceInviteInboundSchema (ဝန်ထမ်းသစ်ဖိတ်ခေါ်ရန် ဒေတာပုံစံ)';
                });
                
                // ၅။ Data Types ပြန်ဆိုခြင်း
                document.querySelectorAll('.prop-type').forEach(el => {
                    if(el.innerText === 'string') el.innerText = 'စာသား (String)';
                    if(el.innerText === 'integer') el.innerText = 'ကိန်းပြည့် (Integer)';
                    if(el.innerText === 'number') el.innerText = 'ဂဏန်း (Number)';
                    if(el.innerText === 'boolean') el.innerText = 'မှန်/မှား (Boolean)';
                });
            }, 1000);
        });
        </script>
        </body>
        """
    )
    return HTMLResponse(content=translated_html, status_code=200)
