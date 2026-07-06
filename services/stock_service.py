from repositories.inventory_repository import InventoryRepository

class StockService:

    @staticmethod
    def get_stock(db, product_id: str, tenant_id: str):

        movements = InventoryRepository.list_by_product(
            db, product_id, tenant_id
        )

        stock = 0

        for m in movements:
            if m.movement_type == "IN":
                stock += m.quantity
            elif m.movement_type == "OUT":
                stock -= m.quantity

        return {
            "product_id": product_id,
            "stock": stock
        }
