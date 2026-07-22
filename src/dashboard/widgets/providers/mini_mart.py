def fast_moving_items_widget(db, current_user=None):
    return {
        "items": [],
        "status": "READY"
    }


def supplier_debt_widget(db, current_user=None):
    return {
        "amount": 0,
        "currency": "MMK"
    }


def daily_profit_widget(db, current_user=None):
    return {
        "profit": 0,
        "currency": "MMK"
    }


def total_revenue_widget(db, current_user=None):
    return {
        "revenue": 0,
        "currency": "MMK"
    }


def payment_methods_widget(db, current_user=None):
    return {
        "cash": 0,
        "cod": 0,
        "transfer": 0
    }


def customer_debt_widget(db, current_user=None):
    return {
        "amount": 0,
        "currency": "MMK"
    }


def expiry_alert_widget(db, current_user=None):
    return {
        "expired": 0,
        "near_expiry": 0
    }


def dead_stock_widget(db, current_user=None):
    return {
        "items": []
    }


def pos_terminal_widget(db, current_user=None):
    return {
        "status": "READY"
    }
