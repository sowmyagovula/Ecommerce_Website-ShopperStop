# 🛍️ ShopperStop - Ecommerce Website

Welcome to **ShopperStop**, a Django-based eCommerce web application designed to provide a simple yet powerful online shopping experience for both buyers and sellers. This project was built with the goal of learning and implementing full-stack web development using Django, Python, and HTML/CSS.

---

## 🔥 Features

### 👤 User Roles
- **Buyer**: Browse products, add to cart, place orders.
- **Seller**: Add/manage product listings, view your own products.

### 🧩 Core Functionalities
- User registration & login
- Role-based UI (Buyer/Seller)
- Add to cart, update quantity, remove items
- Checkout with order summary
- Admin panel to manage product data
- Display products by seller for sellers
- User type displayed on the frontend
- Order storage via `Order` and `OrderItem` models

---

## 🛠️ Tech Stack

- **Backend**: Django, Python
- **Frontend**: HTML, CSS, Bootstrap (optional)
- **Database**: SQLite (default Django DB)
- **Tools**: VS Code, Git, GitHub

---

## 🚀 Getting Started

### 1. Clone the Repository



git clone https://github.com/sowmyagovula/Ecommerce_Website-ShopperStop.git
cd Ecommerce_Website-ShopperStop


### 2. Create a Virtual Environment
python -m venv env
source env/bin/activate  # On Windows: env\Scripts\activate



### 3. Install Dependencies
pip install -r requirements.txt




### 4. Run the Server
python manage.py runserver


### 5. Visit in Browser
http://127.0.0.1:8000/

# 📂 Project Structure

Ecommerce_Website-ShopperStop/
│
├── shopperstop/        # Main Django app
│   ├── models.py        # Product, Order, User models
│   ├── views.py         # Logic for buyers/sellers
│   └── templates/       # HTML templates
│
├── media/              # Uploaded images (if any)
├── static/             # CSS, JS files
├── db.sqlite3          # Database
└── manage.py

###  Future Improvements

- Payment gateway integration

- Product image upload

- Product filters (category, price, etc.)

- Responsive UI with better design


### Acknowledgements
This project was built as a personal learning experience. Thanks to the Django documentation and open-source tutorials that inspired this!

### 📧 Contact
Created by [Sowmya Govula](https://github.com/sowmyagovula/)
