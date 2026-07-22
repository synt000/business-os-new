def appointments_widget(db, current_user=None):
    return {
        "appointments": 0,
        "status": "READY"
    }


def staff_schedule_widget(db, current_user=None):
    return {
        "staff": []
    }


def services_sold_widget(db, current_user=None):
    return {
        "services": []
    }


def customer_return_rate_widget(db, current_user=None):
    return {
        "rate": 0
    }


def top_staff_widget(db, current_user=None):
    return {
        "staff": []
    }


def product_sales_widget(db, current_user=None):
    return {
        "products": []
    }


def revenue_widget(db, current_user=None):
    return {
        "revenue": 0,
        "currency": "MMK"
    }


def no_show_rate_widget(db, current_user=None):
    return {
        "rate": 0
    }


def back_bar_inventory_widget(db, current_user=None):
    return {
        "items": []
    }


def walk_in_checkout_widget(db, current_user=None):
    return {
        "status": "READY"
    }
