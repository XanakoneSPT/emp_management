from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
from datetime import datetime, time, timedelta
from decimal import Decimal

class Department(models.Model):
    name = models.CharField(max_length=100, verbose_name='Tên phòng ban')
    description = models.TextField(blank=True, verbose_name='Mô tả')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Ngày tạo')

    def __str__(self):
        return self.name
    
    class Meta:
        verbose_name = 'Phòng Ban'
        verbose_name_plural = 'Phòng Ban'

class Employee(models.Model):
    POSITION_CHOICES = [
        ('manager', 'Quản Lý'),
        ('team_lead', 'Trưởng Nhóm'),
        ('senior_developer', 'Lập Trình Viên Cao Cấp'),
        ('developer', 'Lập Trình Viên'),
        ('junior_developer', 'Lập Trình Viên Mới'),
        ('hr_manager', 'Trưởng Phòng Nhân Sự'),
        ('hr_executive', 'Nhân Viên Nhân Sự'),
        ('accountant', 'Kế Toán'),
        ('receptionist', 'Lễ Tân'),
        ('office_assistant', 'Trợ Lý Văn Phòng'),
    ]

    user = models.OneToOneField(User, on_delete=models.CASCADE, verbose_name='Người dùng')
    employee_id = models.CharField(max_length=10, unique=True, editable=False, verbose_name='Mã nhân viên')
    department = models.ForeignKey(Department, on_delete=models.SET_NULL, null=True, verbose_name='Phòng ban')
    position = models.CharField(max_length=100, choices=POSITION_CHOICES, verbose_name='Chức vụ')
    phone_number = models.CharField(max_length=15, verbose_name='Số điện thoại')
    address = models.TextField(verbose_name='Địa chỉ')
    face_image = models.ImageField(upload_to='face_images/', verbose_name='Ảnh khuôn mặt')
    face_encoding = models.BinaryField(null=True, blank=True, verbose_name='Mã hóa khuôn mặt')
    joining_date = models.DateField(verbose_name='Ngày vào làm')
    is_active = models.BooleanField(default=True, verbose_name='Đang làm việc')
    
    # Salary related fields
    base_salary = models.DecimalField(max_digits=20, decimal_places=0, default=0, verbose_name='Lương cơ bản')
    hourly_rate = models.DecimalField(max_digits=20, decimal_places=0, default=0, verbose_name='Lương theo giờ')
    overtime_rate = models.DecimalField(max_digits=20, decimal_places=0, default=0, verbose_name='Lương tăng ca')
    standard_work_hours = models.IntegerField(default=8, verbose_name='Số giờ làm tiêu chuẩn')  # Standard hours per day

    class Meta:
        verbose_name = 'Nhân Viên'
        verbose_name_plural = 'Nhân Viên'

    def save(self, *args, **kwargs):
        if not self.employee_id:
            # Generate employee ID only for new employees
            self.employee_id = self.generate_employee_id()
        super().save(*args, **kwargs)

    @staticmethod
    def generate_employee_id():
        prefix = 'EMP'
        last_employee = Employee.objects.order_by('-employee_id').first()
        
        if not last_employee:
            # If no employees exist, start with EMP001
            return f'{prefix}001'
            
        try:
            # Extract the number from the last employee ID
            last_number = int(last_employee.employee_id[3:])
            # Generate the next number
            next_number = last_number + 1
            # Format it back with leading zeros
            return f'{prefix}{next_number:03d}'
        except ValueError:
            # If there's any error in parsing, start with EMP001
            return f'{prefix}001'

    def __str__(self):
        return f"{self.user.get_full_name()} ({self.employee_id})"
    
    def calculate_monthly_salary(self, year, month):
        # Get all attendance records for the specified month
        start_date = datetime(year, month, 1)
        if month == 12:
            end_date = datetime(year + 1, 1, 1)
        else:
            end_date = datetime(year, month + 1, 1)
            
        attendances = self.attendance_set.filter(
            date__gte=start_date.date(),
            date__lt=end_date.date()
        )
        
        total_working_hours = Decimal('0.0')
        overtime_hours = Decimal('0.0')
        total_days = 0
        
        for attendance in attendances:
            if attendance.check_in and attendance.check_out and attendance.status == 'present':
                # Calculate working hours for the day
                duration = attendance.check_out - attendance.check_in
                hours_worked = Decimal(str(duration.total_seconds() / 3600))  # Convert to hours
                
                if hours_worked > Decimal(str(self.standard_work_hours)):
                    overtime = hours_worked - Decimal(str(self.standard_work_hours))
                    overtime_hours += overtime
                    total_working_hours += Decimal(str(self.standard_work_hours))
                else:
                    total_working_hours += hours_worked
                
                total_days += 1
        
        # Calculate salary components
        base_pay = (self.base_salary / Decimal('30')) * Decimal(str(total_days))
        regular_hours_pay = total_working_hours * self.hourly_rate
        overtime_pay = overtime_hours * self.overtime_rate
        
        total_salary = base_pay + regular_hours_pay + overtime_pay
        
        return {
            'total_salary': total_salary,
            'base_pay': base_pay,
            'regular_hours_pay': regular_hours_pay,
            'overtime_pay': overtime_pay,
            'total_days': total_days,
            'total_working_hours': total_working_hours,
            'overtime_hours': overtime_hours
        }

class Attendance(models.Model):
    STATUS_CHOICES = [
        ('present', 'Có mặt'),
        ('absent', 'Vắng mặt'),
        ('late', 'Đi muộn'),
        ('half_day', 'Nửa ngày')
    ]

    employee = models.ForeignKey(Employee, on_delete=models.CASCADE, verbose_name='Nhân viên')
    date = models.DateField(default=timezone.now, verbose_name='Ngày')
    check_in = models.DateTimeField(null=True, blank=True, verbose_name='Giờ vào')
    check_out = models.DateTimeField(null=True, blank=True, verbose_name='Giờ ra')
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, verbose_name='Trạng thái')
    face_confidence = models.FloatField(null=True, blank=True, verbose_name='Độ tin cậy nhận diện')
    
    class Meta:
        unique_together = ['employee', 'date']
        verbose_name = 'Chấm Công'
        verbose_name_plural = 'Chấm Công'

    def __str__(self):
        return f"{self.employee.user.get_full_name()} - {self.date} - {self.get_status_display()}"
    
    def calculate_working_hours(self):
        if self.check_in and self.check_out:
            duration = self.check_out - self.check_in
            return round(duration.total_seconds() / 3600, 2)  # Convert to hours
        return 0

class Salary(models.Model):
    employee = models.ForeignKey(Employee, on_delete=models.CASCADE, verbose_name='Nhân viên')
    year = models.IntegerField(verbose_name='Năm')
    month = models.IntegerField(verbose_name='Tháng')
    base_pay = models.DecimalField(max_digits=20, decimal_places=0, verbose_name='Lương cơ bản')
    regular_hours_pay = models.DecimalField(max_digits=20, decimal_places=0, verbose_name='Lương giờ làm')
    overtime_pay = models.DecimalField(max_digits=20, decimal_places=0, verbose_name='Lương tăng ca')
    total_salary = models.DecimalField(max_digits=20, decimal_places=0, verbose_name='Tổng lương')
    total_days = models.IntegerField(verbose_name='Tổng số ngày')
    total_working_hours = models.DecimalField(max_digits=6, decimal_places=2, verbose_name='Tổng giờ làm')
    overtime_hours = models.DecimalField(max_digits=6, decimal_places=2, verbose_name='Giờ tăng ca')
    generated_at = models.DateTimeField(auto_now_add=True, verbose_name='Ngày tạo')
    
    class Meta:
        unique_together = ['employee', 'year', 'month']
        ordering = ['-year', '-month']
        verbose_name = 'Lương'
        verbose_name_plural = 'Lương'

    def __str__(self):
        return f"{self.employee.user.get_full_name()} - {self.month}/{self.year}"

class Feedback(models.Model):
    FEEDBACK_TYPES = [
        ('suggestion', 'Đề Xuất Cải Thiện'),
        ('issue', 'Báo Cáo Vấn Đề'),
        ('complaint', 'Khiếu Nại'),
        ('other', 'Khác'),
    ]
    
    employee = models.ForeignKey('Employee', on_delete=models.CASCADE, related_name='feedbacks', verbose_name='Nhân viên')
    feedback_type = models.CharField(max_length=20, choices=FEEDBACK_TYPES, verbose_name='Loại phản hồi')
    content = models.TextField(verbose_name='Nội dung')
    submitted_at = models.DateTimeField(auto_now_add=True, verbose_name='Thời gian gửi')
    is_resolved = models.BooleanField(default=False, verbose_name='Đã xử lý')
    resolved_at = models.DateTimeField(null=True, blank=True, verbose_name='Thời gian xử lý')
    resolution_notes = models.TextField(null=True, blank=True, verbose_name='Ghi chú xử lý')
    
    class Meta:
        ordering = ['-submitted_at']
        verbose_name = 'Phản Hồi'
        verbose_name_plural = 'Phản Hồi'
    
    def __str__(self):
        return f"{self.employee.user.get_full_name()} - {self.get_feedback_type_display()} - {self.submitted_at.strftime('%Y-%m-%d %H:%M')}"
    
    def resolve(self, notes=None):
        self.is_resolved = True
        self.resolved_at = timezone.now()
        if notes:
            self.resolution_notes = notes
        self.save()
