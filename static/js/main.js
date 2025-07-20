// Main JavaScript for the clothing store

document.addEventListener('DOMContentLoaded', function() {
    let headerClickCount = 0;
    let clickTimer = null;
    
    // Header click counter for admin access
    const header = document.getElementById('main-header');
    header.addEventListener('click', function() {
        headerClickCount++;
        
        if (clickTimer) {
            clearTimeout(clickTimer);
        }
        
        if (headerClickCount === 3) {
            // Show admin login modal
            const modal = new bootstrap.Modal(document.getElementById('adminLoginModal'));
            modal.show();
            headerClickCount = 0;
            return;
        }
        
        // Reset counter after 2 seconds if not 3 clicks
        clickTimer = setTimeout(() => {
            headerClickCount = 0;
        }, 2000);
    });
    
    // Category filtering
    const categoryButtons = document.querySelectorAll('.btn-category');
    const productItems = document.querySelectorAll('.product-item');
    
    categoryButtons.forEach(button => {
        button.addEventListener('click', function() {
            // Remove active class from all buttons
            categoryButtons.forEach(btn => btn.classList.remove('active'));
            // Add active class to clicked button
            this.classList.add('active');
            
            const category = this.getAttribute('data-category');
            filterProducts(category);
        });
    });
    
    function filterProducts(category) {
        productItems.forEach(item => {
            const itemCategory = item.getAttribute('data-category');
            
            if (category === 'all' || itemCategory === category) {
                item.style.display = 'block';
                item.classList.remove('hidden');
                // Animate in
                setTimeout(() => {
                    item.style.opacity = '1';
                    item.style.transform = 'scale(1)';
                }, 10);
            } else {
                item.classList.add('hidden');
                // Animate out
                item.style.opacity = '0';
                item.style.transform = 'scale(0.8)';
                setTimeout(() => {
                    item.style.display = 'none';
                }, 500);
            }
        });
    }
    
    // Product details toggle
    const detailButtons = document.querySelectorAll('.btn-details');
    detailButtons.forEach(button => {
        button.addEventListener('click', function() {
            const productCard = this.closest('.product-card');
            const details = productCard.querySelector('.product-details');
            
            if (details.style.display === 'none' || details.style.display === '') {
                details.style.display = 'block';
                this.innerHTML = '<i class="fas fa-eye-slash me-1"></i>إخفاء التفاصيل';
                
                // Animate the card expansion
                productCard.style.transition = 'all 0.3s ease';
                setTimeout(() => {
                    details.style.opacity = '1';
                    details.style.transform = 'translateY(0)';
                }, 10);
            } else {
                details.style.display = 'none';
                this.innerHTML = '<i class="fas fa-eye me-1"></i>عرض التفاصيل';
            }
        });
    });
    
    // WhatsApp order functionality
    const orderButtons = document.querySelectorAll('.btn-order');
    orderButtons.forEach(button => {
        button.addEventListener('click', function() {
            const productName = this.getAttribute('data-product-name');
            const productPrice = this.getAttribute('data-product-price');
            const productImage = this.getAttribute('data-product-image');
            
            // Get WhatsApp number from settings
            const whatsappNumber = window.storeSettings?.whatsapp_number || '967700000000';
            
            const message = `السلام عليكم
أريد طلب المنتج التالي:

📦 اسم المنتج: ${productName}
💰 السعر: ${productPrice}
🖼️ صورة المنتج: ${productImage}

شكراً لكم`;
            
            const encodedMessage = encodeURIComponent(message);
            const whatsappUrl = `https://wa.me/${whatsappNumber}?text=${encodedMessage}`;
            
            window.open(whatsappUrl, '_blank');
        });
    });
    
    // Admin login form
    const adminLoginForm = document.getElementById('adminLoginForm');
    if (adminLoginForm) {
        adminLoginForm.addEventListener('submit', function(e) {
            e.preventDefault();
            
            const password = document.getElementById('adminPassword').value;
            const errorDiv = document.getElementById('loginError');
            
            // Show loading
            const submitBtn = document.querySelector('#adminLoginModal .btn-primary');
            const originalText = submitBtn.innerHTML;
            submitBtn.innerHTML = '<span class="loading"></span> جاري التحقق...';
            submitBtn.disabled = true;
            
            fetch('/admin_login', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({ password: password })
            })
            .then(response => response.json())
            .then(data => {
                if (data.success) {
                    window.location.href = '/admin';
                } else {
                    errorDiv.textContent = data.error || 'كلمة مرور خاطئة';
                    errorDiv.classList.remove('d-none');
                }
            })
            .catch(error => {
                console.error('Error:', error);
                errorDiv.textContent = 'حدث خطأ في الاتصال';
                errorDiv.classList.remove('d-none');
            })
            .finally(() => {
                submitBtn.innerHTML = originalText;
                submitBtn.disabled = false;
            });
        });
    }
    
    // Smooth scrolling for anchor links
    document.querySelectorAll('a[href^="#"]').forEach(anchor => {
        anchor.addEventListener('click', function (e) {
            e.preventDefault();
            const target = document.querySelector(this.getAttribute('href'));
            if (target) {
                target.scrollIntoView({
                    behavior: 'smooth',
                    block: 'start'
                });
            }
        });
    });
    
    // Add loading animation to buttons
    function addLoadingToButton(button, originalText) {
        button.innerHTML = `<span class="loading"></span> ${originalText}`;
        button.disabled = true;
    }
    
    function removeLoadingFromButton(button, originalText) {
        button.innerHTML = originalText;
        button.disabled = false;
    }
    
    // Initialize tooltips if Bootstrap is available
    if (typeof bootstrap !== 'undefined') {
        const tooltipTriggerList = [].slice.call(document.querySelectorAll('[data-bs-toggle="tooltip"]'));
        tooltipTriggerList.map(function (tooltipTriggerEl) {
            return new bootstrap.Tooltip(tooltipTriggerEl);
        });
    }
    
    // Add some visual feedback for interactions
    document.addEventListener('click', function(e) {
        // Add ripple effect to buttons
        if (e.target.classList.contains('btn') || e.target.closest('.btn')) {
            const button = e.target.classList.contains('btn') ? e.target : e.target.closest('.btn');
            
            // Create ripple element
            const ripple = document.createElement('span');
            const rect = button.getBoundingClientRect();
            const size = Math.max(rect.width, rect.height);
            const x = e.clientX - rect.left - size / 2;
            const y = e.clientY - rect.top - size / 2;
            
            ripple.style.cssText = `
                position: absolute;
                width: ${size}px;
                height: ${size}px;
                left: ${x}px;
                top: ${y}px;
                background: rgba(255, 255, 255, 0.6);
                border-radius: 50%;
                transform: scale(0);
                animation: ripple 0.6s linear;
                pointer-events: none;
            `;
            
            button.style.position = 'relative';
            button.style.overflow = 'hidden';
            button.appendChild(ripple);
            
            setTimeout(() => {
                ripple.remove();
            }, 600);
        }
    });
    
    // Add ripple animation CSS
    const style = document.createElement('style');
    style.textContent = `
        @keyframes ripple {
            to {
                transform: scale(4);
                opacity: 0;
            }
        }
    `;
    document.head.appendChild(style);
});
