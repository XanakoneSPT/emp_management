from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
from datetime import datetime, time, timedelta
from decimal import Decimal

class Department(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name

class Employee(models.Model):
    POSITION_CHOICES = [
        ('manager', 'Manager'),
        ('team_lead', 'Team Lead'),
        ('senior_developer', 'Senior Developer'),
        ('developer', 'Developer'),
        ('junior_developer', 'Junior Developer'),
        ('hr_manager', 'HR Manager'),
        ('hr_executive', 'HR Executive'),
        ('accountant', 'Accountant'),
        ('receptionist', 'Receptionist'),
        ('office_assistant', 'Office Assistant'),
    ]

    user = models.OneToOneField(User, on_delete=models.CASCADE)
    employee_id = models.CharField(max_length=10, unique=True, editable=False)
    department = models.ForeignKey(Department, on_delete=models.SET_NULL, null=True)
    position = models.CharField(max_length=100, choices=POSITION_CHOICES)
    phone_number = models.CharField(max_length=15)
    address = models.TextField()
    face_image = models.ImageField(upload_to='face_images/')
    face_encoding = models.BinaryField(null=True, blank=True)
    joining_date = models.DateField()
    is_active = models.BooleanField(default=True)
    
    # Salary related fields
    base_salary = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    hourly_rate = models.DecimalField(max_digits=5, decimal_places=2, default=0)
    overtime_rate = models.DecimalField(max_digits=5, decimal_places=2, default=0)
    standard_work_hours = models.IntegerField(default=8)  # Standard hours per day

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
    employee = models.ForeignKey(Employee, on_delete=models.CASCADE)
    date = models.DateField(default=timezone.now)
    check_in = models.DateTimeField(null=True, blank=True)
    check_out = models.DateTimeField(null=True, blank=True)
    status = models.CharField(max_length=20, choices=[
        ('present', 'Present'),
        ('absent', 'Absent'),
        ('late', 'Late'),
        ('half_day', 'Half Day')
    ])
    face_confidence = models.FloatField(null=True, blank=True)
    
    class Meta:
        unique_together = ['employee', 'date']

    def __str__(self):
        return f"{self.employee.user.get_full_name()} - {self.date} - {self.status}"
    
    def calculate_working_hours(self):
        if self.check_in and self.check_out:
            duration = self.check_out - self.check_in
            return round(duration.total_seconds() / 3600, 2)  # Convert to hours
        return 0

class Salary(models.Model):
    employee = models.ForeignKey(Employee, on_delete=models.CASCADE)
    year = models.IntegerField()
    month = models.IntegerField()
    base_pay = models.DecimalField(max_digits=10, decimal_places=2)
    regular_hours_pay = models.DecimalField(max_digits=10, decimal_places=2)
    overtime_pay = models.DecimalField(max_digits=10, decimal_places=2)
    total_salary = models.DecimalField(max_digits=10, decimal_places=2)
    total_days = models.IntegerField()
    total_working_hours = models.DecimalField(max_digits=6, decimal_places=2)
    overtime_hours = models.DecimalField(max_digits=6, decimal_places=2)
    generated_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        unique_together = ['employee', 'year', 'month']
        ordering = ['-year', '-month']

    def __str__(self):
        return f"{self.employee.user.get_full_name()} - {self.month}/{self.year}"
