import os
import json
from flask import Flask, render_template, request, jsonify, redirect, url_for, session
import logging

# Configure logging
logging.basicConfig(level=logging.DEBUG)

app = Flask(__name__)
app.secret_key = os.environ.get("SESSION_SECRET", "your-secret-key-here")

# Data file paths
PRODUCTS_FILE = 'data/products.json'
SETTINGS_FILE = 'data/settings.json'

def load_json_file(filename):
    """Load JSON data from file"""
    try:
        with open(filename, 'r', encoding='utf-8') as f:
            return json.load(f)
    except FileNotFoundError:
        return {}
    except json.JSONDecodeError:
        return {}

def save_json_file(filename, data):
    """Save JSON data to file"""
    os.makedirs(os.path.dirname(filename), exist_ok=True)
    with open(filename, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

def get_default_products():
    """Return default products matching the image"""
    return [
        {
            "id": 1,
            "name": "تيشيرت بياقة دائرية",
            "price": "80 رس",
            "category": "أولاد",
            "image": "https://images.unsplash.com/photo-1521572163474-6864f9cf17ab?w=300&h=300&fit=crop",
            "colors": ["أخضر", "أزرق", "أبيض"],
            "sizes": ["S", "M", "L", "XL"],
            "material": "قطن 100%",
            "description": "تيشيرت مريح بياقة دائرية مناسب للاستخدام اليومي"
        },
        {
            "id": 2,
            "name": "بنطال",
            "price": "120 رس",
            "category": "أولاد",
            "image": "https://images.unsplash.com/photo-1473966968600-fa801b869a1a?w=300&h=300&fit=crop",
            "colors": ["بيج", "كحلي", "أسود"],
            "sizes": ["S", "M", "L", "XL"],
            "material": "قطن وبوليستر",
            "description": "بنطال كاجوال أنيق ومريح"
        },
        {
            "id": 3,
            "name": "تيشيرت",
            "price": "70 رس",
            "category": "بنات",
            "image": "https://images.unsplash.com/photo-1586790170083-2f9ceadc732d?w=300&h=300&fit=crop",
            "colors": ["وردي", "أبيض", "أحمر"],
            "sizes": ["S", "M", "L"],
            "material": "قطن ناعم",
            "description": "تيشيرت نسائي عملي وأنيق"
        },
        {
            "id": 4,
            "name": "سترة مبطنة",
            "price": "250 أولاد",
            "category": "شتوي",
            "image": "https://images.unsplash.com/photo-1544966503-7cc5ac882d5f?w=300&h=300&fit=crop",
            "colors": ["أزرق", "أسود", "رمادي"],
            "sizes": ["S", "M", "L", "XL"],
            "material": "بوليستر مقاوم للماء",
            "description": "سترة شتوية دافئة ومقاومة للرياح"
        }
    ]

def get_default_settings():
    """Return default settings"""
    return {
        "store_name": "مرحبا بكم في متجرنا",
        "whatsapp_number": "966501234567",
        "primary_color": "#87ceeb",
        "font_family": "Cairo",
        "social_links": {
            "facebook": {"url": "https://facebook.com", "visible": True},
            "whatsapp": {"url": "https://wa.me/966501234567", "visible": True},
            "telegram": {"url": "https://t.me/store", "visible": True}
        },
        "delivery_areas": [
            {"name": "الرياض", "active": True},
            {"name": "جدة", "active": True},
            {"name": "الدمام", "active": True}
        ]
    }

@app.route('/')
def index():
    """Main store page"""
    products = load_json_file(PRODUCTS_FILE)
    if not products:
        products = get_default_products()
        save_json_file(PRODUCTS_FILE, products)
    
    settings = load_json_file(SETTINGS_FILE)
    if not settings:
        settings = get_default_settings()
        save_json_file(SETTINGS_FILE, settings)
    
    return render_template('index.html', products=products, settings=settings)

@app.route('/admin_login', methods=['POST'])
def admin_login():
    """Handle admin login"""
    password = request.json.get('password')
    if password == 'F-S-YA76':
        session['admin_logged_in'] = True
        return jsonify({'success': True})
    return jsonify({'success': False, 'error': 'كلمة مرور خاطئة'})

@app.route('/admin')
def admin():
    """Admin panel"""
    if not session.get('admin_logged_in'):
        return redirect(url_for('index'))
    
    products = load_json_file(PRODUCTS_FILE)
    if not products:
        products = get_default_products()
    
    settings = load_json_file(SETTINGS_FILE)
    if not settings:
        settings = get_default_settings()
    
    return render_template('admin.html', products=products, settings=settings)

@app.route('/admin/logout')
def admin_logout():
    """Logout admin"""
    session.pop('admin_logged_in', None)
    return redirect(url_for('index'))

@app.route('/api/products', methods=['GET', 'POST'])
def handle_products():
    """Handle products API"""
    if request.method == 'GET':
        products = load_json_file(PRODUCTS_FILE)
        if not products:
            products = get_default_products()
        return jsonify(products)
    
    elif request.method == 'POST':
        if not session.get('admin_logged_in'):
            return jsonify({'error': 'غير مصرح'}), 403
        
        products = request.json
        save_json_file(PRODUCTS_FILE, products)
        return jsonify({'success': True})

@app.route('/api/settings', methods=['GET', 'POST'])
def handle_settings():
    """Handle settings API"""
    if request.method == 'GET':
        settings = load_json_file(SETTINGS_FILE)
        if not settings:
            settings = get_default_settings()
        return jsonify(settings)
    
    elif request.method == 'POST':
        if not session.get('admin_logged_in'):
            return jsonify({'error': 'غير مصرح'}), 403
        
        settings = request.json
        save_json_file(SETTINGS_FILE, settings)
        return jsonify({'success': True})

@app.route('/filter/<category>')
def filter_products(category):
    """Filter products by category"""
    products = load_json_file(PRODUCTS_FILE)
    if not products:
        products = get_default_products()
    
    if category == 'all':
        filtered_products = products
    else:
        filtered_products = [p for p in products if p['category'] == category]
    
    return jsonify(filtered_products)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
