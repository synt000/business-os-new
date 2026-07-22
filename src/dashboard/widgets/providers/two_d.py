"""
TWO_D_SELLER Dashboard Widgets
Phase: Foundation Provider Layer
"""



def two_d_result_widget(db, tenant_id):
    return {
        "today_results": [],
        "status": "READY"
    }



def commission_widget(db, tenant_id):
    return {
        "today_commission": 0,
        "monthly_commission": 0,
        "currency": "MMK"
    }



def agent_sales_widget(db, tenant_id):
    return {
        "total_agents": 0,
        "today_sales": 0,
        "monthly_sales": 0,
        "currency": "MMK"
    }



def winning_numbers_widget(db, tenant_id):
    return {
        "numbers": [],
        "status": "WAITING"
    }



def hot_numbers_widget(db, tenant_id):
    return {
        "numbers": [],
        "status": "WAITING"
    }



def ticket_sales_widget(db, tenant_id):
    return {
        "total_tickets": 0,
        "sales_amount": 0,
        "currency": "MMK"
    }



def agent_management_widget(db, tenant_id):
    return {
        "total_agents": 0,
        "active_agents": 0
    }



def financial_ledger_widget(db, tenant_id):
    return {
        "income": 0,
        "expense": 0,
        "balance": 0,
        "currency": "MMK"
    }
