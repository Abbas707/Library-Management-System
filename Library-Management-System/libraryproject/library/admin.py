from django.contrib import admin
from library.models import Role, User, Department, Category, Student, Faculty, Librarian, Book, BookRecord

# Register your models here.
admin.site.site_header = "Library Adminn"
admin.site.site_title = "Library admin area"
admin.site.index_title = "Welcome to Library Management System"

admin.site.register(Role)
admin.site.register(User)
admin.site.register(Department)
admin.site.register(Category)
admin.site.register(Student)
admin.site.register(Faculty)
admin.site.register(Librarian)
admin.site.register(Book)
admin.site.register(BookRecord)