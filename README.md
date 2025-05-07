# 💇 OrderSys

A lightweight internal ordering system for multi-branch businesses like salons. Staff can request stock from a central warehouse, and warehouse staff can manage and fulfill those orders.

## ✅ Features

- 🔐 **Login system** with session handling
- 🏪 **Store order dashboard** (view & place orders)
- 📦 **Product search with autocomplete**
- 🧾 **Order detail view**
- ✏️ **Edit order items before fulfillment**
- ✅ **Fulfil orders** (warehouse only)
- 🐳 **Dockerised setup** for easy deployment

---

## 🚀 Getting Started

### 1. Clone and run the project

```bash
git clone https://github.com/GregoryCarberry/ordersys.git
cd ordersys
docker-compose up --build
```

### 2. Seed the database

```bash
docker-compose run backend python -m app.init_db
docker-compose run backend python app/seed_users.py
docker-compose run backend python app/seed_products.py
docker-compose run backend python app/seed_orders.py
```

---

## 👥 Default Users

| Username  | Password     | Role       |
|-----------|--------------|------------|
| root      | changeme123  | root       |
| manager   | password123  | manager    |
| staff     | password123  | staff      |
| warehouse | password123  | warehouse  |

---

## 📁 Project Structure

```
ordersys/
├── backend/
│   └── app/
│       ├── models/
│       ├── templates/
│       ├── db.py
│       ├── init_db.py
│       ├── seed_users.py
│       ├── seed_products.py
│       ├── seed_orders.py
│       └── ...
├── frontend/
│   ├── login.html
│   ├── store_dashboard.html
│   ├── create_order.html
│   ├── order_detail.html
│   └── ...
├── docker-compose.yml
└── README.md
```

---

## 🧭 Roadmap

- [ ] Warehouse dashboard for managing and fulfilling all incoming orders  
- [ ] Granular per-user permission control  
- [ ] Order change/audit tracking  
- [ ] Responsive/mobile-first frontend  
- [ ] Inventory reporting and low-stock alerts  

---

## 🧑‍💻 Author

**Gregory Carberry**  
[LinkedIn](https://www.linkedin.com/in/gregory-carberry/) • [Credly](https://www.credly.com/users/gregory-carberry)

---

## 📄 License

MIT License — use, modify, and contribute freely.