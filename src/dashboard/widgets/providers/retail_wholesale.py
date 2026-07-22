def total_sales_widget(db):
    return {
        "sales": 0,
        "currency": "MMK"
    }


def gross_profit_widget(db):
    return {
        "profit": 0,
        "currency": "MMK"
    }


def retail_wholesale_ratio_widget(db):
    return {
        "retail": 0,
        "wholesale": 0
    }


def average_ticket_widget(db):
    return {
        "average": 0,
        "currency": "MMK"
    }


def inventory_value_widget(db):
    return {
        "value": 0,
        "currency": "MMK"
    }


def wholesale_ledger_widget(db):
    return {
        "entries": []
    }


def customer_credit_widget(db):
    return {
        "amount": 0,
        "currency": "MMK"
    }


def supplier_debt_widget(db):
    return {
        "amount": 0,
        "currency": "MMK"
    }


def purchase_orders_widget(db):
    return {
        "orders": []
    }


def b2b_billing_widget(db):
    return {
        "invoices": []
    }


def retail_pos_widget(db):
    return {
        "status": "READY"
    }


def bulk_price_widget(db):
    return {
        "prices": []
    }


def stock_in_grn_widget(db):
    return {
        "receipts": []
    }
