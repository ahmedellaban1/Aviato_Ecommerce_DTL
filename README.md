# 🛍️ Aviato E-commerce (Django + DTL)

This is a full-featured e-commerce web application built with **Django**, based on the [Aviato HTML Template](https://themefisher.com/products/aviato-ecommerce-template/). The project is designed with:

- 🌐 **Template-based views** (HTML frontend with Django Template Language)
- 🔒 **User authentication** integrated with Django’s session-based login system
- 🛒 **Product listing** and **shopping cart functionality**


---

## ✨ Features

- 🖥️ Beautiful and responsive e-commerce frontend (Aviato template)
- 🔧 Django-based backend with clean project structure
- 🛒 Product listing, categories, and cart-ready frontend
- 🔐 User authentication (login/logout, registration)
- 📊 Admin panel for managing content and inventory

---

## 🔧 Tech Stack

- **Backend**: Django
- **Frontend**: HTML5, CSS3, Bootstrap (Aviato Template)
- **Database**: SQLite (for dev), ready for PostgreSQL
- **Deployment Ready**: Static + media setup for production

---

## 🚀 Getting Started

### For Linux/macOS users:
```bash
# Clone the repo
git clone https://github.com/your-username/aviato-ecommerce.git
cd aviato-ecommerce

# Create virtual environment & activate it
python3 -m venv venv
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Run migrations
python manage.py migrate

# Start development server
python manage.py runserver
```
### For Windows users:

```bash
# Clone the repo
git clone https://github.com/your-username/aviato-ecommerce.git
cd aviato-ecommerce

# Create virtual environment & activate it
python -m venv venv
venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Run migrations
python manage.py migrate

# Start development server
python manage.py runserver
```