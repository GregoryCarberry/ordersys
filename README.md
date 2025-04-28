# Internal Ordering System

[![Branches](https://img.shields.io/badge/branches-main%20%7C%20dev-blue)](https://github.com/GregoryCarberry/ordersys/branches)

---

# OrderSys - Internal Stock Ordering Platform

**OrderSys** is a lightweight, Dockerized internal ordering system designed for businesses with multiple store outlets and a central warehouse.

It provides secure role-based login, store-specific order management, and future-ready inventory tracking using SKUs and barcodes.

---

## How to run

1. Build and start all services:

```bash
docker-compose up --build
```
<br>

2. Access the application:

- Frontend: [http://localhost:3000](http://localhost:3000)
- Backend (API): [http://localhost:5000](http://localhost:5000)

---

## Default credentials (demo users)

| Role    | Username | Password    |
|:--------|:---------|:------------|
| Manager | manager  | password123 |
| Staff   | staff    | password123 |

---

## Current Features

- 🔐 Secure login and logout with session management
- 🛡️ Role-based access control (Managers vs Staff)
- 🛒 Store-specific stock ordering
- 🧠 Session persists cleanly across page refreshes
- 📦 SKU and barcode handling foundation (for future stock system)
- 🐳 Full Docker Compose setup for easy deployment

---

## Tech Stack

- **Frontend:** HTML, CSS, JavaScript
- **Backend:** Python (Flask)
- **Containerization:** Docker, Docker Compose
- **Version Control:** Git (`main` and `dev` branches)

---

## Future Plans

- 📈 Admin dashboard for warehouse stock management
- 🏪 Store dashboards for tracking orders and deliveries
- 📋 SKU/barcode validation for new stock entries
- 📦 Full inventory management system
- 📊 Reporting features (sales, stock levels)

---

> 🚀 This project is under active development on the `dev` branch.  
> Pull requests and contributions are welcome after the core system stabilizes.
