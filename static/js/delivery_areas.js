// Delivery Areas Management for Admin Panel

// Load delivery areas when admin panel loads
function loadDeliveryAreasAdmin() {
    fetch('/api/delivery_areas')
        .then(response => response.json())
        .then(areas => {
            displayDeliveryAreasTable(areas);
        })
        .catch(error => {
            console.error('Error loading delivery areas:', error);
            document.getElementById('deliveryAreasTable').innerHTML = 
                '<div class="alert alert-danger">حدث خطأ في تحميل مناطق التوصيل</div>';
        });
}

// Display delivery areas in admin table
function displayDeliveryAreasTable(areas) {
    const tableContainer = document.getElementById('deliveryAreasTable');
    
    if (areas.length === 0) {
        tableContainer.innerHTML = '<div class="alert alert-info">لا توجد مناطق توصيل مضافة بعد</div>';
        return;
    }
    
    let html = `
        <div class="table-responsive">
            <table class="table table-striped">
                <thead>
                    <tr>
                        <th>اسم المنطقة</th>
                        <th>الحالة</th>
                        <th>الإجراءات</th>
                    </tr>
                </thead>
                <tbody>
    `;
    
    areas.forEach((area) => {
        const statusBadge = area.active ? 
            '<span class="badge bg-success">فعال</span>' : 
            '<span class="badge bg-danger">معطل</span>';
        
        html += `
            <tr>
                <td>${area.name}</td>
                <td>${statusBadge}</td>
                <td>
                    <button class="btn btn-sm btn-primary me-1" onclick="editDeliveryArea(${area.id}, '${area.name}', ${area.active})">
                        <i class="fas fa-edit"></i> تعديل
                    </button>
                    <button class="btn btn-sm btn-danger" onclick="deleteDeliveryArea(${area.id})">
                        <i class="fas fa-trash"></i> حذف
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
    
    tableContainer.innerHTML = html;
}

// Add new delivery area
function addDeliveryArea() {
    document.getElementById('deliveryAreaModalTitle').textContent = 'إضافة منطقة توصيل جديدة';
    document.getElementById('deliveryAreaId').value = '';
    document.getElementById('deliveryAreaName').value = '';
    document.getElementById('deliveryAreaActive').checked = true;
    
    const modal = new bootstrap.Modal(document.getElementById('deliveryAreaModal'));
    modal.show();
}

// Edit delivery area
function editDeliveryArea(id, name, active) {
    document.getElementById('deliveryAreaModalTitle').textContent = 'تعديل منطقة التوصيل';
    document.getElementById('deliveryAreaId').value = id;
    document.getElementById('deliveryAreaName').value = name;
    document.getElementById('deliveryAreaActive').checked = active;
    
    const modal = new bootstrap.Modal(document.getElementById('deliveryAreaModal'));
    modal.show();
}

// Save delivery area
function saveDeliveryArea(event) {
    event.preventDefault();
    
    const id = document.getElementById('deliveryAreaId').value;
    const name = document.getElementById('deliveryAreaName').value.trim();
    const active = document.getElementById('deliveryAreaActive').checked;
    
    if (!name) {
        alert('يرجى إدخال اسم المنطقة');
        return;
    }
    
    const areaData = {
        name: name,
        active: active
    };
    
    if (id !== '') {
        areaData.id = parseInt(id);
    }
    
    fetch('/api/delivery_areas', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify(areaData)
    })
    .then(response => response.json())
    .then(data => {
        if (data.success) {
            bootstrap.Modal.getInstance(document.getElementById('deliveryAreaModal')).hide();
            loadDeliveryAreasAdmin();
            showAlert('تم حفظ منطقة التوصيل بنجاح', 'success');
        } else {
            showAlert(data.error || 'حدث خطأ في حفظ منطقة التوصيل', 'danger');
        }
    })
    .catch(error => {
        console.error('Error saving delivery area:', error);
        showAlert('حدث خطأ في الاتصال', 'danger');
    });
}

// Delete delivery area
function deleteDeliveryArea(id) {
    if (!confirm('هل أنت متأكد من حذف هذه المنطقة؟')) {
        return;
    }
    
    fetch('/api/delivery_areas', {
        method: 'DELETE',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify({ id: id })
    })
    .then(response => response.json())
    .then(data => {
        if (data.success) {
            loadDeliveryAreasAdmin();
            showAlert('تم حذف منطقة التوصيل بنجاح', 'success');
        } else {
            showAlert(data.error || 'حدث خطأ في حذف منطقة التوصيل', 'danger');
        }
    })
    .catch(error => {
        console.error('Error deleting delivery area:', error);
        showAlert('حدث خطأ في الاتصال', 'danger');
    });
}

// Show alert message
function showAlert(message, type) {
    const alertDiv = document.createElement('div');
    alertDiv.className = `alert alert-${type} alert-dismissible fade show`;
    alertDiv.innerHTML = `
        ${message}
        <button type="button" class="btn-close" data-bs-dismiss="alert"></button>
    `;
    
    const container = document.querySelector('.container.py-4');
    container.insertBefore(alertDiv, container.firstChild);
    
    // Auto dismiss after 3 seconds
    setTimeout(() => {
        if (alertDiv.parentNode) {
            alertDiv.remove();
        }
    }, 3000);
}

// Initialize delivery areas management when DOM is loaded
document.addEventListener('DOMContentLoaded', function() {
    // Add delivery area button
    const addDeliveryAreaBtn = document.getElementById('addDeliveryAreaBtn');
    if (addDeliveryAreaBtn) {
        addDeliveryAreaBtn.addEventListener('click', addDeliveryArea);
    }
    
    // Delivery area form submission
    const deliveryAreaForm = document.getElementById('deliveryAreaForm');
    if (deliveryAreaForm) {
        deliveryAreaForm.addEventListener('submit', saveDeliveryArea);
    }
    
    // Load delivery areas when the delivery tab is shown
    const deliveryTab = document.getElementById('delivery-tab');
    if (deliveryTab) {
        deliveryTab.addEventListener('shown.bs.tab', function() {
            loadDeliveryAreasAdmin();
        });
    }
});