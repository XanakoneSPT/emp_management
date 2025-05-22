from django.core.management.base import BaseCommand
from employee.models import Department

class Command(BaseCommand):
    help = 'Creates initial departments in the database'

    def handle(self, *args, **kwargs):
        departments = [
            {
                'name': 'Information Technology',
                'description': 'Software development, IT infrastructure, and technical support'
            },
            {
                'name': 'Human Resources',
                'description': 'Employee management, recruitment, and workplace policies'
            },
            {
                'name': 'Finance',
                'description': 'Financial planning, accounting, and payroll management'
            },
            {
                'name': 'Marketing',
                'description': 'Brand management, marketing strategies, and public relations'
            },
            {
                'name': 'Operations',
                'description': 'Day-to-day operations, logistics, and facility management'
            },
            {
                'name': 'Sales',
                'description': 'Sales strategies, client relationships, and revenue generation'
            },
            {
                'name': 'Research & Development',
                'description': 'Innovation, product development, and market research'
            },
            {
                'name': 'Customer Service',
                'description': 'Customer support, satisfaction, and relationship management'
            }
        ]

        for dept_data in departments:
            department, created = Department.objects.get_or_create(
                name=dept_data['name'],
                defaults={'description': dept_data['description']}
            )
            if created:
                self.stdout.write(
                    self.style.SUCCESS(f'Successfully created department "{dept_data["name"]}"')
                )
            else:
                self.stdout.write(
                    self.style.WARNING(f'Department "{dept_data["name"]}" already exists')
                ) 