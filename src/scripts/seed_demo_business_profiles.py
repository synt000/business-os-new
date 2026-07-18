from src.core.database import SessionLocal
from src.models.business_profile import BusinessProfile
from src.models.saas_core import Tenant


def seed():

    db = SessionLocal()

    try:

        tenant = db.query(Tenant).first()

        if not tenant:
            print("❌ No tenant found")
            return


        demos = [

            {
                "business_slug": "my-online-shop",
                "business_name": "Myanmar Online Shop 🛒",
                "welcome_message": "Welcome to Myanmar Online Shop",
                "description": "Online shopping platform powered by Business OS",
                "theme_color": "#2563eb",
                "owner_name": "Online Shop Owner",
                "owner_phone": "09111111111",
                "phone": "09111111111",
            },


            {
                "business_slug": "golden-2d",
                "business_name": "Golden 2D Seller 🎲",
                "welcome_message": "2D Seller Management",
                "description": "Digital sales management for 2D business",
                "theme_color": "#dc2626",
                "owner_name": "2D Seller",
                "owner_phone": "09222222222",
                "phone": "09222222222",
            },


            {
                "business_slug": "beauty-glow-salon",
                "business_name": "Beauty Glow Salon 💇",
                "welcome_message": "Beauty & Care Service",
                "description": "Salon booking and customer management system",
                "theme_color": "#ec4899",
                "owner_name": "Beauty Owner",
                "owner_phone": "09333333333",
                "phone": "09333333333",
            },


            {
                "business_slug": "shwe-mini-mart",
                "business_name": "Shwe Mini Mart 🏪",
                "welcome_message": "Your Daily Shopping Partner",
                "description": "Inventory and retail management system",
                "theme_color": "#16a34a",
                "owner_name": "Mini Mart Owner",
                "owner_phone": "09444444444",
                "phone": "09444444444",
            },


            {
                "business_slug": "smart-rental-service",
                "business_name": "Smart Rental Service 🏠",
                "welcome_message": "Rental Business Management",
                "description": "Manage rental items, customers and payments",
                "theme_color": "#7c3aed",
                "owner_name": "Rental Owner",
                "owner_phone": "09555555555",
                "phone": "09555555555",
            }

        ]


        for item in demos:

            exists = (
                db.query(BusinessProfile)
                .filter(
                    BusinessProfile.business_slug ==
                    item["business_slug"]
                )
                .first()
            )

            if exists:
                continue


            profile = BusinessProfile(
                tenant_id=str(tenant.id),
                logo_url="https://via.placeholder.com/300",
                cover_url="https://picsum.photos/1200/400",
                is_public=True,
                **item
            )


            db.add(profile)


        db.commit()

        print("✅ Business Profile 5 Types Seed Completed")


    finally:
        db.close()



if __name__ == "__main__":
    seed()
