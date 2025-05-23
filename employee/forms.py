from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from .models import Employee, Department

class EmployeeForm(forms.ModelForm):
    first_name = forms.CharField(
        max_length=30, 
        required=True,
        label='Họ',
        widget=forms.TextInput(attrs={'class': 'form-control'})
    )
    last_name = forms.CharField(
        max_length=30, 
        required=True,
        label='Tên',
        widget=forms.TextInput(attrs={'class': 'form-control'})
    )
    email = forms.EmailField(
        required=True,
        label='Email',
        widget=forms.EmailInput(attrs={'class': 'form-control'})
    )
    username = forms.CharField(
        max_length=30, 
        required=True,
        label='Tên đăng nhập',
        widget=forms.TextInput(attrs={'class': 'form-control'})
    )
    password = forms.CharField(
        widget=forms.PasswordInput(attrs={'class': 'form-control'}),
        required=False,
        label='Mật khẩu'
    )
    confirm_password = forms.CharField(
        widget=forms.PasswordInput(attrs={'class': 'form-control'}),
        required=False,
        label='Xác nhận mật khẩu'
    )
    
    # Override department field to ensure it's required
    department = forms.ModelChoiceField(
        queryset=Department.objects.all(),
        empty_label="Chọn phòng ban",
        required=True,
        label='Phòng ban',
        widget=forms.Select(attrs={'class': 'form-select'})
    )
    
    # Override position field to use the choices from the model
    position = forms.ChoiceField(
        choices=[('', 'Chọn chức vụ')] + list(Employee.POSITION_CHOICES),
        required=True,
        label='Chức vụ',
        widget=forms.Select(attrs={'class': 'form-select'})
    )

    # Face image field
    face_image = forms.ImageField(
        required=False,
        label='Ảnh khuôn mặt',
        widget=forms.FileInput(attrs={'class': 'form-control', 'accept': 'image/*'})
    )

    class Meta:
        model = Employee
        fields = [
            'department', 'position', 'phone_number',
            'address', 'joining_date', 'base_salary', 'hourly_rate',
            'overtime_rate', 'standard_work_hours', 'face_image'
        ]
        widgets = {
            'joining_date': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
            'phone_number': forms.TextInput(attrs={'class': 'form-control'}),
            'address': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
            'base_salary': forms.NumberInput(attrs={'class': 'form-control'}),
            'hourly_rate': forms.NumberInput(attrs={'class': 'form-control'}),
            'overtime_rate': forms.NumberInput(attrs={'class': 'form-control'}),
            'standard_work_hours': forms.NumberInput(attrs={'class': 'form-control'}),
        }
        labels = {
            'phone_number': 'Số điện thoại',
            'address': 'Địa chỉ',
            'joining_date': 'Ngày vào làm',
            'base_salary': 'Lương cơ bản',
            'hourly_rate': 'Lương theo giờ',
            'overtime_rate': 'Lương tăng ca',
            'standard_work_hours': 'Số giờ làm tiêu chuẩn',
        }

    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get('password')
        confirm_password = cleaned_data.get('confirm_password')
        username = cleaned_data.get('username')

        # Check if this is an edit (instance exists) or a new employee
        is_edit = bool(self.instance and self.instance.pk)

        # For new employees, require password
        if not is_edit and not password:
            raise forms.ValidationError("Yêu cầu mật khẩu cho nhân viên mới")

        # If either password field is filled, validate both
        if password or confirm_password:
            if not password:
                raise forms.ValidationError("Vui lòng nhập mật khẩu")
            if not confirm_password:
                raise forms.ValidationError("Vui lòng xác nhận mật khẩu")
            if password != confirm_password:
                raise forms.ValidationError("Mật khẩu không khớp")

        # Check username uniqueness, excluding current user if editing
        username_exists = User.objects.filter(username=username)
        if is_edit:
            username_exists = username_exists.exclude(id=self.instance.user.id)
        
        if username_exists.exists():
            raise forms.ValidationError("Tên đăng nhập đã tồn tại")

        return cleaned_data 