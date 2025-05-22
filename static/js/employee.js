// Department filter auto-submit
document.getElementById('department').addEventListener('change', function() {
    this.form.submit();
});

// Status filter auto-submit
document.getElementById('status').addEventListener('change', function() {
    this.form.submit();
});

// Date range filter auto-submit
document.getElementById('date_from').addEventListener('change', function() {
    if (document.getElementById('date_to').value) {
        this.form.submit();
    }
});

document.getElementById('date_to').addEventListener('change', function() {
    if (document.getElementById('date_from').value) {
        this.form.submit();
    }
});

// Search form submit on enter
document.getElementById('search').addEventListener('keypress', function(e) {
    if (e.key === 'Enter') {
        this.form.submit();
    }
});

// Delete confirmation
document.querySelectorAll('.delete-employee').forEach(button => {
    button.addEventListener('click', function(e) {
        if (!confirm('Bạn có chắc chắn muốn xóa nhân viên này không?')) {
            e.preventDefault();
        }
    });
}); 