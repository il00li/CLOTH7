// Admin panel JavaScript functionality

document.addEventListener('DOMContentLoaded', function() {
    let products = [];
    let settings = {};
    
    // Load initial data
    loadProducts();
    loadSettings();
    
    // Add Product Button
    document.getElementById('addProductBtn').addEventListener('click', function() {
        openProductModal();
    });
    
    // Add Category Button
    document.getElementById('addCategoryBtn').addEventListener('click', function() {
        openCategoryModal();
    });
    
    // Product Form Submit
    document.getElementById('productForm').addEventListener('submit', function(e) {
        e.preventDefault();
        saveProduct();
    });
    
    // Category Form Submit
    document.getElementById('categoryForm').addEventListener('submit', function(e) {
        e.preventDefault();
        saveCategory();
    });
    
    // Settings Form Save
    document.getElementById('saveSettingsBtn').addEventListener('click', function() {
        saveSettings();
    });
    
    // Social Form Save
    document.getElementById('saveSocialBtn').addEventListener('click', function() {
        saveSocialSettings();
    });
    
    function loadProducts() {
        fetch('/api/products')
        .then(response => response.json())
        .then(data => {
            products = data;
            renderProductsTable();
        })
        .catch(error => {
            console.error('Error loading products:', error);
            showAlert('خطأ في تحميل المنتجات', 'danger');
        });
    }
    
    function loadSettings() {
        fetch('/api/settings')
        .then(response => response.json())
        .then(data => {
            settings = data;
            populateSettingsForm();
            renderCategoriesTable();
        })
        .catch(error => {
            console.error('Error loading settings:', error);
            showAlert('خطأ في تحميل الإعدادات', 'danger');
        });
    }
    
    function renderProductsTable() {
        const container = document.getElementById('productsTable');
        
        if (products.length === 0) {
            container.innerHTML = '<p class="text-center text-muted">لا توجد منتجات حالياً</p>';
            return;
        }
        
        let html = `
            <div class="table-responsive">
                <table class="table table-hover">
                    <thead>
                        <tr>
                            <th>الصورة</th>
                            <th>الاسم</th>
                            <th>السعر</th>
                            <th>التصنيف</th>
                            <th>الإجراءات</th>
                        </tr>
                    </thead>
                    <tbody>
        `;
        
        products.forEach(product => {
            html += `
                <tr>
                    <td>
                        <img src="${product.image}" alt="${product.name}" 
                             style="width: 50px; height: 50px; object-fit: cover; border-radius: 8px;">
                    </td>
                    <td>${product.name}</td>
                    <td>${product.price}</td>
                    <td><span class="badge bg-primary">${product.category}</span></td>
                    <td>
                        <button class="btn btn-sm btn-outline-primary me-1" onclick="editProduct(${product.id})">
                            <i class="fas fa-edit"></i>
                        </button>
                        <button class="btn btn-sm btn-outline-danger" onclick="deleteProduct(${product.id})">
                            <i class="fas fa-trash"></i>
                        </button>
                    </td>
                </tr>
            `;
        });
        
        html += `
                    </tbody>
                </table>
            </div>
        `;
        
        container.innerHTML = html;
    }
    
    function renderCategoriesTable() {
        const container = document.getElementById('categoriesTable');
        
        if (!settings.categories || settings.categories.length === 0) {
            container.innerHTML = '<p class="text-center text-muted">لا توجد تصنيفات حالياً</p>';
            return;
        }
        
        let html = `
            <div class="table-responsive">
                <table class="table table-hover">
                    <thead>
                        <tr>
                            <th>الأيقونة</th>
                            <th>اسم التصنيف</th>
                            <th>المعرف</th>
                            <th>الإجراءات</th>
                        </tr>
                    </thead>
                    <tbody>
        `;
        
        settings.categories.forEach(category => {
            html += `
                <tr>
                    <td style="font-size: 1.5rem;">${category.icon || '📦'}</td>
                    <td>${category.name}</td>
                    <td><span class="badge bg-secondary">${category.id}</span></td>
                    <td>
                        <button class="btn btn-sm btn-outline-primary me-1" onclick="editCategory('${category.id}')">
                            <i class="fas fa-edit"></i>
                        </button>
                        <button class="btn btn-sm btn-outline-danger" onclick="deleteCategory('${category.id}')">
                            <i class="fas fa-trash"></i>
                        </button>
                    </td>
                </tr>
            `;
        });
        
        html += `
                    </tbody>
                </table>
            </div>
        `;
        
        container.innerHTML = html;
    }
    
    function openProductModal(product = null) {
        const modal = new bootstrap.Modal(document.getElementById('productModal'));
        const form = document.getElementById('productForm');
        
        if (product) {
            // Editing existing product
            document.getElementById('productModalTitle').textContent = 'تعديل المنتج';
            document.getElementById('productId').value = product.id;
            document.getElementById('productName').value = product.name;
            document.getElementById('productPrice').value = product.price;
            document.getElementById('productCategory').value = product.category;
            document.getElementById('productImage').value = product.image;
            document.getElementById('productColors').value = product.colors.join(', ');
            document.getElementById('productSizes').value = product.sizes.join(', ');
            document.getElementById('productMaterial').value = product.material;
            document.getElementById('productDescription').value = product.description;
        } else {
            // Adding new product
            document.getElementById('productModalTitle').textContent = 'إضافة منتج جديد';
            form.reset();
            document.getElementById('productId').value = '';
        }
        
        modal.show();
    }
    
    function openCategoryModal(category = null) {
        const modal = new bootstrap.Modal(document.getElementById('categoryModal'));
        const form = document.getElementById('categoryForm');
        
        if (category) {
            // Editing existing category
            document.getElementById('categoryModalTitle').textContent = 'تعديل التصنيف';
            document.getElementById('categoryId').value = category.id;
            document.getElementById('categoryName').value = category.name;
            document.getElementById('categoryIcon').value = category.icon || '';
        } else {
            // Adding new category
            document.getElementById('categoryModalTitle').textContent = 'إضافة تصنيف جديد';
            form.reset();
            document.getElementById('categoryId').value = '';
        }
        
        modal.show();
    }
    
    function saveCategory() {
        const categoryId = document.getElementById('categoryId').value || generateCategoryId();
        const categoryName = document.getElementById('categoryName').value;
        const categoryIcon = document.getElementById('categoryIcon').value || '📦';
        
        const categoryData = {
            id: categoryId,
            name: categoryName,
            icon: categoryIcon
        };
        
        if (!settings.categories) {
            settings.categories = [];
        }
        
        const isEditing = document.getElementById('categoryId').value !== '';
        
        if (isEditing) {
            // Update existing category
            const index = settings.categories.findIndex(c => c.id === categoryId);
            if (index !== -1) {
                settings.categories[index] = categoryData;
            }
        } else {
            // Add new category
            settings.categories.push(categoryData);
        }
        
        // Save to server
        fetch('/api/settings', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify(settings)
        })
        .then(response => response.json())
        .then(data => {
            if (data.success) {
                showAlert(isEditing ? 'تم تحديث التصنيف بنجاح' : 'تم إضافة التصنيف بنجاح', 'success');
                renderCategoriesTable();
                updateProductCategoryOptions();
                bootstrap.Modal.getInstance(document.getElementById('categoryModal')).hide();
            } else {
                throw new Error(data.error || 'خطأ في الحفظ');
            }
        })
        .catch(error => {
            console.error('Error saving category:', error);
            showAlert('خطأ في حفظ التصنيف', 'danger');
        });
    }
    
    function generateCategoryId() {
        const name = document.getElementById('categoryName').value;
        return name.toLowerCase().replace(/\s+/g, '_').replace(/[^\w\u0600-\u06FF]/g, '');
    }
    
    function updateProductCategoryOptions() {
        const categorySelect = document.getElementById('productCategory');
        if (categorySelect && settings.categories) {
            categorySelect.innerHTML = '';
            settings.categories.forEach(category => {
                const option = document.createElement('option');
                option.value = category.name;
                option.textContent = category.name;
                categorySelect.appendChild(option);
            });
        }
    }
    
    function saveProduct() {
        const formData = {
            id: document.getElementById('productId').value || Date.now(),
            name: document.getElementById('productName').value,
            price: document.getElementById('productPrice').value,
            category: document.getElementById('productCategory').value,
            image: document.getElementById('productImage').value,
            colors: document.getElementById('productColors').value.split(',').map(c => c.trim()).filter(c => c),
            sizes: document.getElementById('productSizes').value.split(',').map(s => s.trim()).filter(s => s),
            material: document.getElementById('productMaterial').value,
            description: document.getElementById('productDescription').value
        };
        
        const isEditing = document.getElementById('productId').value !== '';
        
        if (isEditing) {
            // Update existing product
            const index = products.findIndex(p => p.id == formData.id);
            if (index !== -1) {
                products[index] = formData;
            }
        } else {
            // Add new product
            formData.id = parseInt(formData.id);
            products.push(formData);
        }
        
        // Save to server
        fetch('/api/products', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify(products)
        })
        .then(response => response.json())
        .then(data => {
            if (data.success) {
                showAlert(isEditing ? 'تم تحديث المنتج بنجاح' : 'تم إضافة المنتج بنجاح', 'success');
                renderProductsTable();
                bootstrap.Modal.getInstance(document.getElementById('productModal')).hide();
            } else {
                throw new Error(data.error || 'خطأ في الحفظ');
            }
        })
        .catch(error => {
            console.error('Error saving product:', error);
            showAlert('خطأ في حفظ المنتج', 'danger');
        });
    }
    
    function populateSettingsForm() {
        document.getElementById('storeName').value = settings.store_name || '';
        document.getElementById('whatsappNumber').value = settings.whatsapp_number || '';
        document.getElementById('primaryColor').value = settings.primary_color || '#87ceeb';
        document.getElementById('fontFamily').value = settings.font_family || 'Cairo';
        
        // Update categories for product form
        updateProductCategoryOptions();
        
        // Social links
        if (settings.social_links) {
            document.getElementById('facebookUrl').value = settings.social_links.facebook?.url || '';
            document.getElementById('facebookVisible').checked = settings.social_links.facebook?.visible || false;
            document.getElementById('telegramUrl').value = settings.social_links.telegram?.url || '';
            document.getElementById('telegramVisible').checked = settings.social_links.telegram?.visible || false;
        }
        
        // Apply current settings to CSS
        updateCSSVariables();
    }
    
    function saveSettings() {
        const updatedSettings = {
            ...settings,
            store_name: document.getElementById('storeName').value,
            whatsapp_number: document.getElementById('whatsappNumber').value,
            primary_color: document.getElementById('primaryColor').value,
            font_family: document.getElementById('fontFamily').value
        };
        
        fetch('/api/settings', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify(updatedSettings)
        })
        .then(response => response.json())
        .then(data => {
            if (data.success) {
                settings = updatedSettings;
                showAlert('تم حفظ الإعدادات بنجاح', 'success');
                // Update CSS variables
                updateCSSVariables();
            } else {
                throw new Error(data.error || 'خطأ في الحفظ');
            }
        })
        .catch(error => {
            console.error('Error saving settings:', error);
            showAlert('خطأ في حفظ الإعدادات', 'danger');
        });
    }
    
    function saveSocialSettings() {
        const updatedSettings = {
            ...settings,
            social_links: {
                facebook: {
                    url: document.getElementById('facebookUrl').value,
                    visible: document.getElementById('facebookVisible').checked
                },
                whatsapp: {
                    url: `https://wa.me/${settings.whatsapp_number}`,
                    visible: true
                },
                telegram: {
                    url: document.getElementById('telegramUrl').value,
                    visible: document.getElementById('telegramVisible').checked
                }
            }
        };
        
        fetch('/api/settings', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify(updatedSettings)
        })
        .then(response => response.json())
        .then(data => {
            if (data.success) {
                settings = updatedSettings;
                showAlert('تم حفظ إعدادات التواصل الاجتماعي بنجاح', 'success');
            } else {
                throw new Error(data.error || 'خطأ في الحفظ');
            }
        })
        .catch(error => {
            console.error('Error saving social settings:', error);
            showAlert('خطأ في حفظ إعدادات التواصل', 'danger');
        });
    }
    
    function updateCSSVariables() {
        const root = document.documentElement;
        root.style.setProperty('--primary-color', settings.primary_color);
        root.style.setProperty('--glass-bg', `${settings.primary_color}1a`);
        root.style.setProperty('--glass-border', `${settings.primary_color}4d`);
        root.style.setProperty('--font-family', settings.font_family);
        
        // Load new font if different
        const currentFont = settings.font_family;
        if (currentFont && !document.querySelector(`link[href*="${currentFont}"]`)) {
            const fontLink = document.createElement('link');
            fontLink.href = `https://fonts.googleapis.com/css2?family=${currentFont}:wght@200;300;400;600;700&display=swap`;
            fontLink.rel = 'stylesheet';
            document.head.appendChild(fontLink);
        }
    }
    
    function showAlert(message, type = 'info') {
        // Create alert element
        const alert = document.createElement('div');
        alert.className = `alert alert-${type} alert-dismissible fade show position-fixed`;
        alert.style.cssText = 'top: 20px; right: 20px; z-index: 9999; max-width: 400px;';
        alert.innerHTML = `
            ${message}
            <button type="button" class="btn-close" data-bs-dismiss="alert"></button>
        `;
        
        document.body.appendChild(alert);
        
        // Auto remove after 5 seconds
        setTimeout(() => {
            if (alert.parentNode) {
                alert.remove();
            }
        }, 5000);
    }
    
    // Global functions for product management
    window.editProduct = function(id) {
        const product = products.find(p => p.id === id);
        if (product) {
            openProductModal(product);
        }
    };
    
    // Global functions for category management
    window.editCategory = function(id) {
        const category = settings.categories?.find(c => c.id === id);
        if (category) {
            openCategoryModal(category);
        }
    };
    
    window.deleteCategory = function(id) {
        if (confirm('هل أنت متأكد من حذف هذا التصنيف؟ سيؤثر ذلك على المنتجات المرتبطة به.')) {
            if (!settings.categories) return;
            
            settings.categories = settings.categories.filter(c => c.id !== id);
            
            fetch('/api/settings', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify(settings)
            })
            .then(response => response.json())
            .then(data => {
                if (data.success) {
                    showAlert('تم حذف التصنيف بنجاح', 'success');
                    renderCategoriesTable();
                    updateProductCategoryOptions();
                } else {
                    throw new Error(data.error || 'خطأ في الحذف');
                }
            })
            .catch(error => {
                console.error('Error deleting category:', error);
                showAlert('خطأ في حذف التصنيف', 'danger');
            });
        }
    };
    
    window.deleteProduct = function(id) {
        if (confirm('هل أنت متأكد من حذف هذا المنتج؟')) {
            products = products.filter(p => p.id !== id);
            
            fetch('/api/products', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify(products)
            })
            .then(response => response.json())
            .then(data => {
                if (data.success) {
                    showAlert('تم حذف المنتج بنجاح', 'success');
                    renderProductsTable();
                } else {
                    throw new Error(data.error || 'خطأ في الحذف');
                }
            })
            .catch(error => {
                console.error('Error deleting product:', error);
                showAlert('خطأ في حذف المنتج', 'danger');
            });
        }
    };
    
    // Auto-save functionality
    const autoSaveFields = ['storeName', 'whatsappNumber', 'primaryColor', 'fontFamily'];
    autoSaveFields.forEach(fieldId => {
        const field = document.getElementById(fieldId);
        if (field) {
            field.addEventListener('change', debounce(saveSettings, 1000));
        }
    });
    
    // Debounce function
    function debounce(func, wait) {
        let timeout;
        return function executedFunction(...args) {
            const later = () => {
                clearTimeout(timeout);
                func(...args);
            };
            clearTimeout(timeout);
            timeout = setTimeout(later, wait);
        };
    }
    
    // Real-time color preview
    document.getElementById('primaryColor').addEventListener('input', function() {
        const color = this.value;
        const root = document.documentElement;
        root.style.setProperty('--primary-color', color);
        root.style.setProperty('--glass-bg', `${color}1a`);
        root.style.setProperty('--glass-border', `${color}4d`);
    });
    
    // Real-time font preview
    document.getElementById('fontFamily').addEventListener('change', function() {
        const font = this.value;
        const root = document.documentElement;
        root.style.setProperty('--font-family', font);
        
        // Load new font if different
        if (!document.querySelector(`link[href*="${font}"]`)) {
            const fontLink = document.createElement('link');
            fontLink.href = `https://fonts.googleapis.com/css2?family=${font}:wght@200;300;400;600;700&display=swap`;
            fontLink.rel = 'stylesheet';
            document.head.appendChild(fontLink);
        }
    });
    
    // Keyboard shortcuts
    document.addEventListener('keydown', function(e) {
        // Ctrl+N: Add new product
        if (e.ctrlKey && e.key === 'n') {
            e.preventDefault();
            document.getElementById('addProductBtn').click();
        }
        
        // Ctrl+S: Save settings
        if (e.ctrlKey && e.key === 's') {
            e.preventDefault();
            saveSettings();
        }
    });
});
