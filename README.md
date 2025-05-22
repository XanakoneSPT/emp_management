# Hệ Thống Quản Lý Nhân Viên (Employee Management System)

Một hệ thống quản lý nhân viên toàn diện được xây dựng bằng Django, tích hợp chấm công bằng nhận diện khuôn mặt và quản lý lương.

## Tính Năng Chính

### 1. Quản Lý Nhân Viên
- Thêm, sửa, xóa thông tin nhân viên
- Quản lý thông tin cá nhân và nghề nghiệp
- Phân loại theo phòng ban
- Tìm kiếm và lọc nhân viên

### 2. Chấm Công
- Chấm công tự động bằng nhận diện khuôn mặt
- Chấm công thủ công với nhiều trạng thái (Có mặt, Vắng mặt, Đi muộn, Nửa ngày)
- Xem lịch sử chấm công
- Báo cáo chi tiết theo ngày/tháng

### 3. Quản Lý Lương
- Tính lương tự động dựa trên giờ làm
- Tính lương tăng ca
- Xem chi tiết lương theo tháng
- Xuất báo cáo lương

## Yêu Cầu Hệ Thống

- Python 3.8+
- Django 4.2+
- OpenCV
- face_recognition
- Các thư viện khác (xem requirements.txt)

## Cài Đặt

1. Clone repository:
```bash
git clone https://github.com/your-username/employee-management.git
cd employee-management
```

2. Tạo và kích hoạt môi trường ảo:
```bash
python -m venv venv
source venv/bin/activate  # Linux/Mac
venv\Scripts\activate     # Windows
```

3. Cài đặt các thư viện cần thiết:
```bash
pip install -r requirements.txt
```

4. Thực hiện migrate database:
```bash
python manage.py migrate
```

5. Tạo tài khoản admin:
```bash
python manage.py createsuperuser
```

6. Chạy server:
```bash
python manage.py runserver
```

## Cấu Trúc Thư Mục

```
employee_management/
├── employee/                 # Ứng dụng chính
│   ├── models.py            # Định nghĩa database
│   ├── views.py             # Logic xử lý
│   ├── urls.py             # URL routing
│   └── templates/          # Templates
├── static/                  # File tĩnh (CSS, JS)
├── media/                   # File upload
├── requirements.txt         # Thư viện cần thiết
└── manage.py               # File quản lý Django
```

## Sử Dụng

1. Đăng nhập với tài khoản admin
2. Thêm phòng ban và nhân viên
3. Đăng ký khuôn mặt cho nhân viên
4. Bắt đầu sử dụng chấm công và quản lý

## Bảo Mật

- Mã hóa mật khẩu
- Phân quyền người dùng
- Xác thực khuôn mặt an toàn
- Bảo vệ dữ liệu nhân viên

## Đóng Góp

Mọi đóng góp đều được hoan nghênh! Vui lòng:

1. Fork repository
2. Tạo branch mới (`git checkout -b feature/AmazingFeature`)
3. Commit thay đổi (`git commit -m 'Add some AmazingFeature'`)
4. Push to branch (`git push origin feature/AmazingFeature`)
5. Tạo Pull Request

## Giấy Phép

Phân phối theo giấy phép MIT. Xem `LICENSE` để biết thêm thông tin.

## Liên Hệ

Your Name - email@example.com

Project Link: https://github.com/your-username/employee-management 