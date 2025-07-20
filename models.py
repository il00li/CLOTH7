from app import db
import json
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import Integer, String, Text
from datetime import datetime

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
            self.colors_json = json.dumps(colors, ensure_ascii=False)
        elif isinstance(colors, str):
            if ',' in colors:
                colors_list = [c.strip() for c in colors.split(',') if c.strip()]
                self.colors_json = json.dumps(colors_list, ensure_ascii=False)
            else:
                self.colors_json = json.dumps([colors], ensure_ascii=False)

    def get_colors(self):
        """الحصول على الألوان كقائمة"""
        if self.colors_json:
            try:
                colors = json.loads(self.colors_json)
                if isinstance(colors, list):
                    return colors
                return [str(colors)]
            except:
                return [self.colors_json] if self.colors_json else []
        return []

    def set_sizes(self, sizes):
        """تحديد المقاسات المتوفرة"""
        if isinstance(sizes, list):
            self.sizes_json = json.dumps(sizes, ensure_ascii=False)
        elif isinstance(sizes, str):
            if ',' in sizes:
                sizes_list = [s.strip() for s in sizes.split(',') if s.strip()]
                self.sizes_json = json.dumps(sizes_list, ensure_ascii=False)
            else:
                self.sizes_json = json.dumps([sizes], ensure_ascii=False)

    def get_sizes(self):
        """الحصول على المقاسات كقائمة"""
        if self.sizes_json:
            try:
                sizes = json.loads(self.sizes_json)
                if isinstance(sizes, list):
                    return sizes
                return [str(sizes)]
            except:
                return [self.sizes_json] if self.sizes_json else []
        return []

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