from django.urls import path
from . import views

app_name = 'employee'

urlpatterns = [
    path('', views.dashboard, name='dashboard'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('employees/', views.employee_list, name='employee_list'),
    path('employees/add/', views.add_employee, name='add_employee'),
    path('employees/<int:employee_id>/edit/', views.edit_employee, name='edit_employee'),
    path('employees/<int:employee_id>/delete/', views.delete_employee, name='delete_employee'),
    path('employees/export/', views.export_employee_list, name='export_employee_list'),
    path('manage-attendance/', views.manage_attendance, name='manage_attendance'),
    path('manage-attendance/<int:employee_id>/mark/', views.admin_mark_attendance, name='admin_mark_attendance'),
    path('manage-attendance/<int:employee_id>/face/', views.admin_register_face, name='admin_register_face'),
    path('manage-attendance/delete/<int:attendance_id>/', views.admin_delete_attendance, name='admin_delete_attendance'),
    path('attendance/', views.attendance_list, name='attendance_list'),
    path('attendance/export/', views.export_attendance_list, name='export_attendance_list'),
    path('salary/', views.salary_list, name='salary_list'),
    path('salary/export/', views.export_salary_list, name='export_salary_list'),
    path('salary/generate/', views.generate_salary, name='generate_salary'),
    path('salary/<int:salary_id>/', views.salary_detail, name='salary_detail'),
    path('auto-attendance/', views.auto_mark_attendance, name='auto_mark_attendance'),
    path('process-auto-attendance/', views.process_auto_attendance, name='process_auto_attendance'),
    path('regenerate-face-encoding/<int:employee_id>/', views.regenerate_face_encoding, name='regenerate_face_encoding'),
    path('departments/', views.department_list, name='department_list'),
] 