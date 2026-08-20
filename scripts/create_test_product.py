from app.db.session import SessionLocal
from app.models.product import Product


db = SessionLocal()

try:
    product = Product(
        name="Arroz basmati"
    )

    db.add(product)
    db.commit()
    db.refresh(product)

    print(
        f"Producto creado: {product.id} - {product.name}"
    )

finally:
    db.close()
