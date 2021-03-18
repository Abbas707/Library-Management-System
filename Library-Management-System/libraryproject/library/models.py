from django.db import models
from django.contrib.auth.models import User, AbstractUser
from phonenumber_field.modelfields import PhoneNumberField
import datetime
from django.template.defaultfilters import truncatechars

# Create your models here.

class Department(models.Model):
  DEPARTMENT = (
    ('Computer', 'Computer'),
    ('IT', 'IT'), 
    ('Mechanical','Mechanical'),
    ('Civil', 'Civil'),
    ('Electrical', 'Electrical'),
    ('Environmental', 'Environmental'),
  )
  department = models.CharField(max_length=250, choices=DEPARTMENT, blank=True, null= True)

  def __str__(self):
    return self.department


class Category(models.Model):

  CATEGORY = (
		('History', 'History'),
		('Technical', 'Technical'),
		('Educational', 'Educational'),
		('Biography', 'Biography'),
		('Cooking', 'Cooking'),
	)
	
  category = models.CharField(max_length=250, choices=CATEGORY, blank=True,null=True)

  def __str__(self):
    return self.category



class Role(models.Model):
  TYPE = (
    ('Student','Student'),
    ('Faculty','Faculty'),
    ('Librarian','Librarian'),
    )
  role = models.CharField(max_length=50, choices=TYPE,blank=True, null=True)

  def __str__(self):
    return self.role


class User(AbstractUser):
  role = models.ForeignKey(Role, on_delete=models.CASCADE, blank=True, null=True)
  phone_no = PhoneNumberField(null=True, blank=True, unique=True)
  profile_pic = models.ImageField(upload_to='profile_pic',blank=True, null=True)
  department = models.ForeignKey(Department, related_name='dept',on_delete=models.CASCADE,blank=True, null=True)


class Admin(models.Model):
  user = models.OneToOneField(User, on_delete=models.CASCADE, blank=True, null=True)

  def __str__(self):
    return self.user.username

    
class Student(models.Model):
  user = models.OneToOneField(User, on_delete=models.CASCADE)

  def __str__(self):
    return self.user.username


class Faculty(models.Model):
  user = models.OneToOneField(User, on_delete=models.CASCADE)
  
  def __str__(self):
    return self.user.username


class Librarian(models.Model):
  user = models.OneToOneField(User, on_delete=models.CASCADE)

  def __str__(self):
    return self.user.username


class Book(models.Model):
  title = models.CharField(max_length=250)
  category = models.ForeignKey(Category,on_delete=models.CASCADE, blank=True, null=True)
  author = models.CharField(max_length=250, blank=True, null=True)
  description = models.CharField(max_length=500, blank=True, null=True)
  no_of_copy = models.BigIntegerField(default=None,blank=True, null=True)
  available_copy = models.BigIntegerField(default=None,blank=True, null=True)
  cover_pic = models.ImageField(upload_to='bookcover_pic',blank=True, null=True)
  
  def __str__(self):
    return self.title
    
  @property
  def short_description(self):
    return truncatechars(self.description, 50)

class BookRecord(models.Model):
  book = models.ForeignKey(Book, on_delete=models.CASCADE, blank=True, null=True)
  user = models.ForeignKey(User, on_delete=models.CASCADE,blank=True, null=True)
  issue_date = models.DateField(auto_now_add=True,blank=True, null=True)
  due_date = models.DateField(default=None,blank=True, null=True)
  return_date = models.DateField(auto_now_add=True,blank=True, null=True)
  
  def __str__(self):
    return self.book_name

  def book_due_date(self):
    self.due_date = self.issue_date + datetime.timedelta(days=10)
