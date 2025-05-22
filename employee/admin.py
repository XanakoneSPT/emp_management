from django.contrib import admin
from .models import Department, Employee, Attendance, Salary

@admin.register(Department)
class DepartmentAdmin(admin.ModelAdmin):
    list_display = ('name', 'created_at')
    search_fields = ('name',)

@admin.register(Employee)
class EmployeeAdmin(admin.ModelAdmin):
    list_display = ('employee_id', 'get_full_name', 'department', 'position', 'base_salary', 'hourly_rate', 'is_active')
    list_filter = ('department', 'is_active')
    search_fields = ('employee_id', 'user__first_name', 'user__last_name')
    fieldsets = (
        ('Basic Information', {
            'fields': ('user', 'employee_id', 'department', 'position', 'is_active', 'joining_date')
        }),
        ('Contact Information', {
            'fields': ('phone_number', 'address')
        }),
        ('Salary Information', {
            'fields': ('base_salary', 'hourly_rate', 'overtime_rate', 'standard_work_hours')
        }),
        ('Face Recognition', {
            'fields': ('face_image', 'face_encoding')
        }),
    )
    
    def get_full_name(self, obj):
        return obj.user.get_full_name()
    get_full_name.short_description = 'Full Name'

@admin.register(Attendance)
class AttendanceAdmin(admin.ModelAdmin):
    list_display = ('employee', 'date', 'status', 'check_in', 'check_out', 'get_working_hours')
    list_filter = ('date', 'status')
    search_fields = ('employee__user__first_name', 'employee__user__last_name', 'employee__employee_id')
    date_hierarchy = 'date'
    
    def get_working_hours(self, obj):
        return f"{obj.calculate_working_hours():.2f} hours"
    get_working_hours.short_description = 'Working Hours'

@admin.register(Salary)
class SalaryAdmin(admin.ModelAdmin):
    list_display = ('employee', 'year', 'month', 'total_salary', 'total_days', 'total_working_hours', 'overtime_hours')
    list_filter = ('year', 'month')
    search_fields = ('employee__user__first_name', 'employee__user__last_name', 'employee__employee_id')
    date_hierarchy = 'generated_at'
    readonly_fields = ('generated_at',)
