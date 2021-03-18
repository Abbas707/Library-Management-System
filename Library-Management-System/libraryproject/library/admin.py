from django.contrib import admin
from library.models import Role, User, Department, Category, Student, Faculty, Librarian, Book, BookRecord, Admin

# Register your models here.
admin.site.site_header = "Library Admin"
admin.site.site_title = "Library admin area"
admin.site.index_title = "Welcome to Library Management System"

admin.site.register(Department)
admin.site.register(Category)
admin.site.register(Role)
admin.site.register(Student)
admin.site.register(Faculty)
admin.site.register(Librarian)
admin.site.register(BookRecord)
admin.site.register(Admin)

class BookAdmin(admin.ModelAdmin):
  list_display = ('title', 'category', 'short_description', 'author', 'cover_pic')
  search_fields = ('title',)
admin.site.register(Book, BookAdmin)

class UserAdmin(admin.ModelAdmin):
  list_display = ('first_name', 'last_name', 'username', 'phone_no', 'profile_pic', 'role', 'department')
  ordering = ('role',)
  search_fields = ('username',)
admin.site.register(User, UserAdmin)

