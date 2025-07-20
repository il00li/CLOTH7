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
from app import db
import json
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import Integer, String, Text

class Product(db.Model):
    __tablename__ = 'products'
    
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    name: Mapped[str] = mapped_column(String(200), nullable=False)
    price: Mapped[str] = mapped_column(String(100), nullable=False)
    category: Mapped[str] = mapped_column(String(100), nullable=False)
    image_path: Mapped[str] = mapped_column(String(500), nullable=True)
    material: Mapped[str] = mapped_column(String(200), nullable=True)
    description: Mapped[str] = mapped_column(Text, nullable=True)
    colors_json: Mapped[str] = mapped_column(Text, nullable=True)
    sizes_json: Mapped[str] = mapped_column(Text, nullable=True)
    
    def set_colors(self, colors):
        """تحديد الألوان المتوفرة"""
        if isinstance(colors, list):
            self.colors_json = json.dumps(colors)
        elif isinstance(colors, str):
            # إذا كانت النصوص مفصولة بفواصل
            if ',' in colors:
                colors_list = [c.strip() for c in colors.split(',')]
                self.colors_json = json.dumps(colors_list)
            else:
                self.colors_json = json.dumps([colors])
    
    def get_colors(self):
        """الحصول على الألوان كقائمة"""
        if self.colors_json:
            try:
                colors = json.loads(self.colors_json)
                if isinstance(colors, list):
                    return ', '.join(colors)
                return str(colors)
            except:
                return self.colors_json or ''
        return ''
    
    def set_sizes(self, sizes):
        """تحديد المقاسات المتوفرة"""
        if isinstance(sizes, list):
            self.sizes_json = json.dumps(sizes)
        elif isinstance(sizes, str):
            # إذا كانت النصوص مفصولة بفواصل
            if ',' in sizes:
                sizes_list = [s.strip() for s in sizes.split(',')]
                self.sizes_json = json.dumps(sizes_list)
            else:
                self.sizes_json = json.dumps([sizes])
    
    def get_sizes(self):
        """الحصول على المقاسات كنص"""
        if self.sizes_json:
            try:
                sizes = json.loads(self.sizes_json)
                if isinstance(sizes, list):
                    return ', '.join(sizes)
                return str(sizes)
            except:
                return self.sizes_json or ''
        return ''

    @property
    def colors(self):
        """خاصية للحصول على الألوان للعرض في القالب"""
        return self.get_colors()
    
    @property
    def sizes(self):
        """خاصية للحصول على المقاسات للعرض في القالب"""
        return self.get_sizes()

    @property
    def image(self):
        """خاصية للحصول على رابط الصورة"""
        return self.image_path or ''

class StoreSettings(db.Model):
    __tablename__ = 'store_settings'
    
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    store_name: Mapped[str] = mapped_column(String(200), default="متجر الملابس العربي")
    whatsapp_number: Mapped[str] = mapped_column(String(20), default="967700000000")
    primary_color: Mapped[str] = mapped_column(String(7), default="#87ceeb")
    font_family: Mapped[str] = mapped_column(String(100), default="Cairo")
    currency: Mapped[str] = mapped_column(String(50), default="ريال يمني")
    categories_json: Mapped[str] = mapped_column(Text, nullable=True)
    social_links_json: Mapped[str] = mapped_column(Text, nullable=True)
    delivery_areas_json: Mapped[str] = mapped_column(Text, nullable=True)
    
    def set_categories(self, categories):
        """تحديد الفئات"""
        self.categories_json = json.dumps(categories, ensure_ascii=False)
    
    def get_categories(self):
        """الحصول على الفئات"""
        if self.categories_json:
            try:
                return json.loads(self.categories_json)
            except:
                pass
        return [
            {"name": "أولاد", "icon": "👦", "active": True},
            {"name": "بنات", "icon": "👧", "active": True},
            {"name": "شتوي", "icon": "🧥", "active": True}
        ]
    
    def set_social_links(self, social_links):
        """تحديد روابط التواصل الاجتماعي"""
        self.social_links_json = json.dumps(social_links, ensure_ascii=False)
    
    def get_social_links(self):
        """الحصول على روابط التواصل الاجتماعي"""
        if self.social_links_json:
            try:
                return json.loads(self.social_links_json)
            except:
                pass
        return {
            "facebook": {"url": "", "visible": False},
            "whatsapp": {"url": f"https://wa.me/{self.whatsapp_number}", "visible": True},
            "telegram": {"url": "", "visible": False}
        }
    
    def set_delivery_areas(self, delivery_areas):
        """تحديد مناطق التوصيل"""
        self.delivery_areas_json = json.dumps(delivery_areas, ensure_ascii=False)
    
    def get_delivery_areas(self):
        """الحصول على مناطق التوصيل"""
        if self.delivery_areas_json:
            try:
                return json.loads(self.delivery_areas_json)
            except:
                pass
        return [
            {"id": 1, "name": "صنعاء", "active": True},
            {"id": 2, "name": "عدن", "active": True},
            {"id": 3, "name": "تعز", "active": True},
            {"id": 4, "name": "الحديدة", "active": True}
        ]

# للتوافق مع النسخة القديمة
Settings = StoreSettings
