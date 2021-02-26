from django.db import models
from django.contrib.auth.models import AbstractUser
import datetime
from phonenumber_field.modelfields import PhoneNumberField


# Create your models here.
class Role(models.Model):
  TYPE = (
        ('Student','Student'),
        ('Faculty','Faculty'),
        ('Librarian','Librarian'),
        ('Admin', 'Admin'),
  )
  type = models.CharField(max_length=255, choices=TYPE, blank=True, null=True)


class User(AbstractUser):
  role = models.ForeignKey(Role, on_delete=models.CASCADE, blank=True, null=True)
  phone_no = PhoneNumberField(null=True, blank=True, unique=True)
  address = models.TextField(max_length=255)
  profile_pic = models.ImageField(upload_to='profile_pic', default='goku.jpeg', blank=True, null=True)


class Department(models.Model):
	DEPT = (
		('Computer', 'Computer'),
		('IT', 'IT'),
		('Mechanical','Mechanical'),
		('Civil', 'Civil'),
		('Electrical', 'Electrical'),
		('Environmental', 'Environmental'),
	)
	dept = models.CharField(max_length=255, choices=DEPT, blank=True, null= True)


class Category(models.Model):
	CAT = (
		('History', 'History'),
		('Technical', 'Technical'),
		('Educational', 'Educational'),
		('Biography', 'Biography'),
		('Cooking', 'Cooking'),
	)
	cat = models.CharField(max_length=255, choices=CAT, blank=True, null= True)


class Student(models.Model):
  user = models.OneToOneField(User, on_delete=models.CASCADE, blank=True, null=True)
  department = models.ForeignKey(Department, on_delete=models.CASCADE, blank=True, null=True)

  def __str__(self):
    return self.user.username


class Faculty(models.Model):
  user = models.OneToOneField(User, on_delete=models.CASCADE, blank=True, null=True)
  department = models.ForeignKey(Department, on_delete=models.CASCADE, blank=True, null=True)
  
  def __str__(self):
    return self.user.username


class Librarian(models.Model):
  user = models.OneToOneField(User, on_delete=models.CASCADE, blank=True, null=True)

  def __str__(self):
    return user.username


class Admin(models.Model):
  user = models.OneToOneField(User, on_delete=models.CASCADE, blank=True, null=True)

  def __str__(self):
    return self.user.username


class Book(models.Model):
  category = models.ForeignKey(Category, on_delete=models.CASCADE, blank=True, null=True)
  title = models.CharField(max_length=250)
  author = models.CharField(max_length=250)
  description = models.CharField(max_length=255, blank=True, null=True)
  published_date = models.DateField(auto_now_add=False, blank=True, null=True)
  no_of_copy = models.BigIntegerField(default=None)
  available_copy = models.BigIntegerField(default=None)
  
  def __str__(delf):
    return self.title
    
    
class BookRecord(models.Model):
  book = models.ForeignKey(Book, on_delete=models.CASCADE, blank=True, null=True)
  user = models.ForeignKey(User, on_delete=models.CASCADE, blank=True, null=True)
  issue_date = models.DateField(auto_now_add=True)
  return_date = models.DateField(auto_now_add=True)
  due_date = models.DateField(default=None)
  
  def __str__(self):
    return self.book_name

  def book_due_date(self):
    self.due_date = self.issue_date + datetime.timedelta(days=10)


