from app import db
from datetime import datetime
import json

class Product(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(200), nullable=False)
    price = db.Column(db.String(100), nullable=False)
    category = db.Column(db.String(100), nullable=False)
    image_path = db.Column(db.String(500))  # Path to uploaded image
    colors = db.Column(db.Text)  # JSON string of colors
    sizes = db.Column(db.Text)   # JSON string of sizes
    material = db.Column(db.String(200))
    description = db.Column(db.Text)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    def get_colors(self):
        if self.colors:
            return json.loads(self.colors)
        return []
    
    def set_colors(self, colors_list):
        self.colors = json.dumps(colors_list, ensure_ascii=False)
    
    def get_sizes(self):
        if self.sizes:
            return json.loads(self.sizes)
        return []
    
    def set_sizes(self, sizes_list):
        self.sizes = json.dumps(sizes_list, ensure_ascii=False)

class Settings(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    store_name = db.Column(db.String(200), default="مرحبا بكم في متجرنا")
    whatsapp_number = db.Column(db.String(20), default="967700000000")
    primary_color = db.Column(db.String(10), default="#87ceeb")
    font_family = db.Column(db.String(50), default="Cairo")
    currency = db.Column(db.String(50), default="ريال يمني")
    categories = db.Column(db.Text)  # JSON string
    social_links = db.Column(db.Text)  # JSON string
    delivery_areas = db.Column(db.Text)  # JSON string
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    def get_categories(self):
        if self.categories:
            return json.loads(self.categories)
        return [
            {"id": "boys", "name": "أولاد", "icon": "👦"},
            {"id": "girls", "name": "بنات", "icon": "👧"},
            {"id": "winter", "name": "شتوي", "icon": "❄️"}
        ]
    
    def set_categories(self, categories_list):
        self.categories = json.dumps(categories_list, ensure_ascii=False)
    
    def get_social_links(self):
        if self.social_links:
            return json.loads(self.social_links)
        return {
            "facebook": {"url": "https://facebook.com", "visible": True},
            "whatsapp": {"url": f"https://wa.me/{self.whatsapp_number}", "visible": True},
            "telegram": {"url": "https://t.me/store", "visible": True}
        }
    
    def set_social_links(self, links_dict):
        self.social_links = json.dumps(links_dict, ensure_ascii=False)
    
    def get_delivery_areas(self):
        if self.delivery_areas:
            return json.loads(self.delivery_areas)
        return [
            {"name": "صنعاء", "active": True},
            {"name": "عدن", "active": True},
            {"name": "تعز", "active": True},
            {"name": "الحديدة", "active": True}
        ]
    
    def set_delivery_areas(self, areas_list):
        self.delivery_areas = json.dumps(areas_list, ensure_ascii=False)