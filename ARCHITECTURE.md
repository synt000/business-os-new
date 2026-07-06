# BUSINESS OS - ARCHITECTURE

---

## 🧠 SYSTEM DESIGN

Clean Architecture + DDD

Router → Service → Repository → Database

---

## 🏗 CORE PRINCIPLES

- Multi-tenant isolation via tenant_id
- JWT-based authentication
- Strict layer separation
- No direct DB access from router

---

## 🔐 AUTH DESIGN

- JWT contains:
  - user_id
  - tenant_id
  - role
- RBAC enforced at service layer

---

## 📦 MODULES

### Product
- Create / List / Update

### Category
- Category management

### Inventory
- IN / OUT movement system
- Stock calculated from ledger

---

## 🚀 DEPLOYMENT TARGET

- Docker
- Render / VPS
- Stateless FastAPI service
