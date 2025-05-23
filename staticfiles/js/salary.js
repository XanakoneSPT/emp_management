// Month filter auto-submit
document.getElementById('month').addEventListener('change', function() {
    this.form.submit();
});

// Department filter auto-submit
document.getElementById('department').addEventListener('change', function() {
    this.form.submit();
});

// Search form submit on enter
document.getElementById('search').addEventListener('keypress', function(e) {
    if (e.key === 'Enter') {
        this.form.submit();
    }
});

// Format currency
function formatCurrency(amount) {
    return new Intl.NumberFormat('vi-VN', {
        style: 'currency',
        currency: 'VND'
    }).format(amount);
}

// Update all currency displays
document.querySelectorAll('.currency').forEach(element => {
    const amount = parseInt(element.textContent.replace(/[^0-9]/g, ''));
    element.textContent = formatCurrency(amount);
}); 