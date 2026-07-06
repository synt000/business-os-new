import csv
import io
from sqlalchemy.orm import Session
from domains.product.model import Product
from uuid import UUID

class ExportService:
    @staticmethod
    def generate_product_csv(db: Session, tenant_id: UUID):
        products = db.query(Product).filter(Product.tenant_id == tenant_id).all()
        
        output = io.StringIO()
        writer = csv.writer(output)
        writer.writerow(["ID", "Name", "SKU", "Price"])
        
        for p in products:
            writer.writerow([p.id, p.name, p.sku, p.price])
            
        output.seek(0)
        return output
