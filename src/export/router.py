from fastapi import APIRouter, Depends, Request
from fastapi.responses import StreamingResponse
from sqlalchemy.orm import Session
from infrastructure.db.session import get_db
from services.export_service import ExportService
import io

router = APIRouter(prefix="/export", tags=["export"])

@router.get("/products")
def export_products(request: Request, db: Session = Depends(get_db)):
    csv_data = ExportService.generate_product_csv(db, request.state.tenant_id)
    return StreamingResponse(
        io.StringIO(csv_data.getvalue()),
        media_type="text/csv",
        headers={"Content-Disposition": "attachment; filename=products.csv"}
    )
