# BUSINESS OS

Production-grade multi-tenant ERP backend built with FastAPI.

---

## 🚀 Overview

- JWT Authentication
- RBAC
- Multi-Tenant System
- Inventory Movement (IN/OUT)
- Product & Category modules
- Prometheus metrics ready

---

## 🏗 Architecture

Router → Service → Repository → Database

---

## ⚙️ Tech Stack

- FastAPI
- SQLAlchemy
- Pydantic v1
- python-jose
- prometheus-client

---

## 🧪 Run (Local)

uvicorn apps.main:app --reload --host 0.0.0.0 --port 8000

