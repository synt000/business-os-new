from src.core.database import SessionLocal
from src.domains.rental.models import RentalPlan


db=SessionLocal()


plans=[
    ("Starter",50000),
    ("Business",150000),
    ("Enterprise",500000)
]


for name,price in plans:

    exists=db.query(RentalPlan)\
    .filter(RentalPlan.name==name)\
    .first()

    if not exists:

        db.add(
            RentalPlan(
                name=name,
                monthly_price=price,
                trial_days="14"
            )
        )


db.commit()

print("Rental Seed Done")
