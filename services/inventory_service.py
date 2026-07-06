from domains.product.inventory_model import Inventory
from repositories.inventory_repository import InventoryRepository

class InventoryService:

    @staticmethod
    def add_stock(db, product_id: str, quantity: float, tenant_id: str):

        movement = Inventory(
            product_id=product_id,
            movement_type="IN",
            quantity=quantity,
            tenant_id=tenant_id
        )

        return InventoryRepository.add_movement(db, movement)

    @staticmethod
    def remove_stock(db, product_id: str, quantity: float, tenant_id: str):

        movement = Inventory(
            product_id=product_id,
            movement_type="OUT",
            quantity=quantity,
            tenant_id=tenant_id
        )

        return InventoryRepository.add_movement(db, movement)

    @staticmethod
    def history(db, product_id: str, tenant_id: str):
        return InventoryRepository.list_by_product(db, product_id, tenant_id)
