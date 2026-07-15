print("=== Loading Models Test ===")

from src.models.saas_core import Product as OldProduct
print("Old Product OK:", OldProduct)

from src.domains.product.models import Product as NewProduct
print("New Product OK:", NewProduct)

from src.domains.category.models import Category as NewCategory
print("New Category OK:", NewCategory)

print("DONE")
