from src.models.saas_core import Order

def ad_roi_widget(db, tenant_id):
    revenue = (
        db.query(Order)
        .filter(Order.tenant_id == tenant_id)
        .with_entities(Order.total_amount)
        .all()
    )

    total_revenue = sum(r[0] or 0 for r in revenue)

    # Placeholder until Meta/TikTok Ads integration
    ad_spend = 0.0

    roi = 0.0
    if ad_spend > 0:
        roi = round(((total_revenue - ad_spend) / ad_spend) * 100, 2)

    return {
        "ad_spend": ad_spend,
        "revenue": total_revenue,
        "roi_percent": roi,
        "currency": "MMK",
        "status": "PLACEHOLDER"
    }
