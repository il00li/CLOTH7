import os
import json
from flask import Flask, render_template, request, jsonify, redirect, url_for, session, flash
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import DeclarativeBase
from werkzeug.utils import secure_filename
from werkzeug.middleware.proxy_fix import ProxyFix
import logging

# Configure logging
logging.basicConfig(level=logging.DEBUG)

class Base(DeclarativeBase):
    pass

db = SQLAlchemy(model_class=Base)

# create the app
app = Flask(__name__)
app.secret_key = os.environ.get("SESSION_SECRET", "your-secret-key-here")
app.wsgi_app = ProxyFix(app.wsgi_app, x_proto=1, x_host=1)

# configure the database
database_url = os.environ.get("DATABASE_URL")
if database_url and database_url.startswith("postgres://"):
    database_url = database_url.replace("postgres://", "postgresql://", 1)
app.config["SQLALCHEMY_DATABASE_URI"] = database_url or "sqlite:///store.db"
app.config["SQLALCHEMY_ENGINE_OPTIONS"] = {
    "pool_recycle": 300,
    "pool_pre_ping": True,
}

# File upload configuration
UPLOAD_FOLDER = 'static/uploads'
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif', 'webp'}
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # 16MB max file size

# initialize the app with the extension
db.init_app(app)

# Ensure upload directory exists
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def get_or_create_settings():
    """Get existing settings or create default ones"""
    settings = models.StoreSettings.query.first()
    if not settings:
        settings = models.StoreSettings(
            store_name="متجر الملابس العربي",
            whatsapp_number="967700000000",
            primary_color="#87ceeb",
            font_family="Cairo",
            currency="ريال يمني"
        )
        # Set default categories
        settings.set_categories([
            {"name": "أولاد", "icon": "👦", "active": True},
            {"name": "بنات", "icon": "👧", "active": True},
            {"name": "شتوي", "icon": "🧥", "active": True}
        ])
        # Set default social links
        settings.set_social_links({
            "facebook": {"url": "", "visible": False},
            "whatsapp": {"url": f"https://wa.me/{settings.whatsapp_number}", "visible": True},
            "telegram": {"url": "", "visible": False}
        })
        # Set default delivery areas
        settings.set_delivery_areas([
            {"id": 1, "name": "صنعاء", "active": True},
            {"id": 2, "name": "عدن", "active": True},
            {"id": 3, "name": "تعز", "active": True},
            {"id": 4, "name": "الحديدة", "active": True}
        ])
        db.session.add(settings)
        db.session.commit()
    return settings

with app.app_context():
    # Import models after db is initialized
    import models
    db.create_all()

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
        "whatsapp_number": "967700000000",
        "primary_color": "#87ceeb",
        "font_family": "Cairo",
        "currency": "ريال يمني",
        "categories": [
            {"id": "boys", "name": "أولاد", "icon": "👦"},
            {"id": "girls", "name": "بنات", "icon": "👧"},
            {"id": "winter", "name": "شتوي", "icon": "❄️"}
        ],
        "social_links": {
            "facebook": {"url": "https://facebook.com", "visible": True},
            "whatsapp": {"url": "https://wa.me/967700000000", "visible": True},
            "telegram": {"url": "https://t.me/store", "visible": True}
        },
        "delivery_areas": [
            {"name": "صنعاء", "active": True},
            {"name": "عدن", "active": True},
            {"name": "تعز", "active": True},
            {"name": "الحديدة", "active": True}
        ]
    }

@app.route('/')
def index():
    """Main store page"""
    products = models.Product.query.all()
    if not products:
        # Create default products
        default_products = get_default_products()
        for prod_data in default_products:
            product = models.Product(
                name=prod_data['name'],
                price=prod_data['price'],
                category=prod_data['category'],
                image_path=prod_data['image'],
                material=prod_data['material'],
                description=prod_data['description']
            )
            product.set_colors(prod_data['colors'])
            product.set_sizes(prod_data['sizes'])
            db.session.add(product)
        db.session.commit()
        products = models.Product.query.all()
    
    settings = get_or_create_settings()
    
    # Convert settings to dictionary for template
    settings_dict = {
        'store_name': settings.store_name,
        'whatsapp_number': settings.whatsapp_number,
        'primary_color': settings.primary_color,
        'font_family': settings.font_family,
        'currency': settings.currency,
        'categories': settings.get_categories(),
        'social_links': settings.get_social_links(),
        'delivery_areas': settings.get_delivery_areas()
    }
    
    return render_template('index.html', products=products, settings=settings_dict)

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
    
    products = models.Product.query.all()
    settings = get_or_create_settings()
    
    # Convert to dictionary format for template
    settings_dict = {
        'store_name': settings.store_name,
        'whatsapp_number': settings.whatsapp_number,
        'primary_color': settings.primary_color,
        'font_family': settings.font_family,
        'currency': settings.currency,
        'categories': settings.get_categories(),
        'social_links': settings.get_social_links(),
        'delivery_areas': settings.get_delivery_areas()
    }
    
    return render_template('admin.html', products=products, settings=settings_dict)

@app.route('/admin/logout')
def admin_logout():
    """Logout admin"""
    session.pop('admin_logged_in', None)
    return redirect(url_for('index'))

@app.route('/api/products', methods=['GET', 'POST'])
def handle_products():
    """Handle products API"""
    if request.method == 'GET':
        products = models.Product.query.all()
        products_data = []
        for product in products:
            products_data.append({
                'id': product.id,
                'name': product.name,
                'price': product.price,
                'category': product.category,
                'image': product.image_path,
                'colors': product.get_colors(),
                'sizes': product.get_sizes(),
                'material': product.material or '',
                'description': product.description or ''
            })
        return jsonify(products_data)
    
    elif request.method == 'POST':
        if not session.get('admin_logged_in'):
            return jsonify({'error': 'غير مصرح'}), 403
        
        try:
            product_data = request.json
            
            if 'id' in product_data and product_data['id']:
                # Update existing product
                product = models.Product.query.get(product_data['id'])
                if not product:
                    return jsonify({'error': 'المنتج غير موجود'}), 404
                    
                product.name = product_data['name']
                product.price = product_data['price']
                product.category = product_data['category']
                product.image_path = product_data.get('image', product.image_path)
                product.material = product_data.get('material', '')
                product.description = product_data.get('description', '')
                product.set_colors(product_data.get('colors', []))
                product.set_sizes(product_data.get('sizes', []))
            else:
                # Create new product
                product = models.Product(
                    name=product_data['name'],
                    price=product_data['price'],
                    category=product_data['category'],
                    image_path=product_data.get('image', ''),
                    material=product_data.get('material', ''),
                    description=product_data.get('description', '')
                )
                product.set_colors(product_data.get('colors', []))
                product.set_sizes(product_data.get('sizes', []))
                db.session.add(product)
            
            db.session.commit()
            return jsonify({'success': True})
            
        except Exception as e:
            db.session.rollback()
            logging.error(f"Error saving product: {str(e)}")
            return jsonify({'error': f'خطأ في حفظ المنتج: {str(e)}'}), 500

@app.route('/api/settings', methods=['GET', 'POST'])
def handle_settings():
    """Handle settings API"""
    if request.method == 'GET':
        settings = get_or_create_settings()
        settings_dict = {
            'store_name': settings.store_name,
            'whatsapp_number': settings.whatsapp_number,
            'primary_color': settings.primary_color,
            'font_family': settings.font_family,
            'currency': settings.currency,
            'categories': settings.get_categories(),
            'social_links': settings.get_social_links(),
            'delivery_areas': settings.get_delivery_areas()
        }
        return jsonify(settings_dict)
    
    elif request.method == 'POST':
        if not session.get('admin_logged_in'):
            return jsonify({'error': 'غير مصرح'}), 403
        
        settings_data = request.json
        settings = get_or_create_settings()
        
        # Update settings
        settings.store_name = settings_data.get('store_name', settings.store_name)
        settings.whatsapp_number = settings_data.get('whatsapp_number', settings.whatsapp_number)
        settings.primary_color = settings_data.get('primary_color', settings.primary_color)
        settings.font_family = settings_data.get('font_family', settings.font_family)
        settings.currency = settings_data.get('currency', settings.currency)
        
        if 'categories' in settings_data:
            settings.set_categories(settings_data['categories'])
        if 'social_links' in settings_data:
            settings.set_social_links(settings_data['social_links'])
        if 'delivery_areas' in settings_data:
            settings.set_delivery_areas(settings_data['delivery_areas'])
        
        db.session.commit()
        return jsonify({'success': True})

@app.route('/upload_image', methods=['POST'])
def upload_image():
    """Handle image upload"""
    if not session.get('admin_logged_in'):
        return jsonify({'error': 'غير مصرح'}), 403
    
    if 'file' not in request.files:
        return jsonify({'error': 'لم يتم اختيار ملف'}), 400
    
    file = request.files['file']
    if file.filename == '':
        return jsonify({'error': 'لم يتم اختيار ملف'}), 400
    
    if file and allowed_file(file.filename):
        filename = secure_filename(file.filename)
        # Add timestamp to avoid conflicts
        import time
        timestamp = str(int(time.time()))
        name, ext = filename.rsplit('.', 1)
        filename = f"{name}_{timestamp}.{ext}"
        
        file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        file.save(file_path)
        
        # Return the URL path for the image
        image_url = url_for('static', filename=f'uploads/{filename}')
        return jsonify({'success': True, 'image_url': image_url})
    
    return jsonify({'error': 'نوع الملف غير مدعوم'}), 400

@app.route('/api/delivery_areas', methods=['GET', 'POST', 'DELETE'])
def handle_delivery_areas():
    """Handle delivery areas management"""
    if request.method == 'GET':
        settings = get_or_create_settings()
        areas = settings.get_delivery_areas()
        # Ensure each area has an ID
        for i, area in enumerate(areas):
            if 'id' not in area:
                area['id'] = i + 1
        return jsonify(areas)
    
    elif request.method == 'POST':
        if not session.get('admin_logged_in'):
            return jsonify({'error': 'غير مصرح'}), 403
        
        area_data = request.json
        settings = get_or_create_settings()
        areas = settings.get_delivery_areas()
        
        # Ensure areas have IDs
        for i, area in enumerate(areas):
            if 'id' not in area:
                area['id'] = i + 1
        
        if 'id' in area_data and area_data['id']:
            # Update existing area
            found = False
            for i, area in enumerate(areas):
                if area.get('id') == area_data['id']:
                    areas[i] = {
                        'id': area_data['id'],
                        'name': area_data['name'],
                        'active': area_data['active']
                    }
                    found = True
                    break
            if not found:
                return jsonify({'error': 'المنطقة غير موجودة'}), 404
        else:
            # Add new area
            new_id = max([area.get('id', 0) for area in areas] + [0]) + 1
            new_area = {
                'id': new_id,
                'name': area_data['name'],
                'active': area_data['active']
            }
            areas.append(new_area)
        
        settings.set_delivery_areas(areas)
        db.session.commit()
        return jsonify({'success': True})
    
    elif request.method == 'DELETE':
        if not session.get('admin_logged_in'):
            return jsonify({'error': 'غير مصرح'}), 403
        
        area_id = request.json.get('id')
        settings = get_or_create_settings()
        areas = settings.get_delivery_areas()
        
        # Remove area with matching ID
        areas = [area for area in areas if area.get('id') != area_id]
        
        settings.set_delivery_areas(areas)
        db.session.commit()
        return jsonify({'success': True})

@app.route('/api/products/<int:product_id>', methods=['DELETE'])
def delete_product(product_id):
    """Delete a product"""
    if not session.get('admin_logged_in'):
        return jsonify({'error': 'غير مصرح'}), 403
    
    product = models.Product.query.get_or_404(product_id)
    db.session.delete(product)
    db.session.commit()
    return jsonify({'success': True})

@app.route('/filter/<category>')
def filter_products(category):
    """Filter products by category"""
    products = models.Product.query.all()
    
    if category == 'all':
        filtered_products = products
    else:
        filtered_products = [p for p in products if p.category == category]
    
    # Convert to dict format
    products_data = []
    for product in filtered_products:
        products_data.append({
            'id': product.id,
            'name': product.name,
            'price': product.price,
            'category': product.category,
            'image': product.image_path,
            'colors': product.get_colors(),
            'sizes': product.get_sizes(),
            'material': product.material,
            'description': product.description
        })
    
    return jsonify(products_data)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
