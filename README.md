# 🛒 NexusCart API

![FastAPI](https://img.shields.io/badge/FastAPI-005571?style=for-the-badge&logo=fastapi)
![PostgreSQL](https://img.shields.io/badge/PostgreSQL-316192?style=for-the-badge&logo=postgresql&logoColor=white)
![SQLAlchemy](https://img.shields.io/badge/SQLAlchemy-D71F26?style=for-the-badge&logo=redhat&logoColor=white)

NexusCart is a high-performance, asynchronous RESTful inventory management API built using **FastAPI** and backed by a **PostgreSQL** relational database. By leveraging **SQLAlchemy ORM**, the system abstractly manages data entities with strict data integrity, type safety, and real-time validations.

---

## 🚀 Key Highlights

* ⚙️ **Lifecycle-Managed DB Seeding:** Utilizes FastAPI's modern `lifespan` context manager to safely check and seed mock catalog inventory only when the database is empty on application startup.
* 🛡️ **Robust Pydantic Data Validation:** Incoming request payloads are strictly validated against strong types before ever interacting with the database layer, throwing explicit client errors.
* 🔄 **Standardized REST HTTP Status Responses:** Adheres closely to explicit REST paradigms, delivering proper native HTTP headers and status structures (e.g., `201 Created` for additions, `404 Not Found` exceptions for missing keys).
* 📝 **Automated Swagger Documentation:** Inherits automatic openAPI specification modeling. Simply run the app to instantly access interactive UI testing dashboards.

---

## 📂 Project Architecture

```text
├── __pycache__/          # Compiled python bytecode configurations
├── database.py           # Engine deployment and database session connections
├── database_models.py    # SQLAlchemy Relational ORM Schemas (PostgreSQL Tables)
├── main.py               # Core application routing, hooks, and controller loops
└── models.py             # Pydantic data modeling for validation and serialization
