def total_sales_widget(db, current_user=None):
    return {
        "sales": 0,
        "currency": "MMK"
    }


def gross_profit_widget(db, current_user=None):
    return {
        "profit": 0,
        "currency": "MMK"
    }


def retail_wholesale_ratio_widget(db, current_user=None):
    return {
        "retail": 0,
        "wholesale": 0
    }


def average_ticket_widget(db, current_user=None):
    return {
        "average": 0,
        "currency": "MMK"
    }


def inventory_value_widget(db, current_user=None):
    return {
        "value": 0,
        "currency": "MMK"
    }


def wholesale_ledger_widget(db, current_user=None):
    return {
        "entries": []
    }


def customer_credit_widget(db, current_user=None):
    return {
        "amount": 0,
        "currency": "MMK"
    }


def supplier_debt_widget(db, current_user=None):
    return {
        "amount": 0,
        "currency": "MMK"
    }


def purchase_orders_widget(db, current_user=None):
    return {
        "orders": []
    }


def b2b_billing_widget(db, current_user=None):
    return {
        "invoices": []
    }


def retail_pos_widget(db, current_user=None):
    return {
        "status": "READY"
    }


def bulk_price_widget(db, current_user=None):
    return {
        "prices": []
    }


def stock_in_grn_widget(db, current_user=None):
    return {
        "receipts": []
    }
