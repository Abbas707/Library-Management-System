from django import forms
from library.models import *
from django.core.exceptions import ValidationError
from django.core import validators
from django.contrib.auth.forms import UserCreationForm

  
class UserForm(UserCreationForm):
  first_name = forms.CharField(widget=forms.TextInput(attrs={'placeholder':'Enter first name'}))
  last_name = forms.CharField(widget=forms.TextInput(attrs={'placeholder':'Enter last name'}))
  username = forms.CharField(widget=forms.TextInput(attrs={'placeholder':'Enter username'}))
  password1 = forms.CharField(label='Password', widget=forms.PasswordInput(attrs={'placeholder':'Enter Password'}))
  password2 = forms.CharField(label='Confirm Password', widget=forms.PasswordInput(attrs={'placeholder':'Confirm Password'}))
  phone_no = forms.CharField(widget=forms.TextInput(attrs={'placeholder':'Enter contact number'}))

  class Meta:
    model = User
    fields = ('role', 'department', 'first_name', 'last_name', 'username', 'password1','password2','phone_no', 'profile_pic',)


class UserFormOne(forms.ModelForm):
  first_name = forms.CharField(widget=forms.TextInput(attrs={'placeholder':'Enter first name'}))
  last_name = forms.CharField(widget=forms.TextInput(attrs={'placeholder':'Enter last name'}))
  username = forms.CharField(widget=forms.TextInput(attrs={'placeholder':'Enter username'}))
  phone_no = forms.CharField(widget=forms.TextInput(attrs={'placeholder':'Enter contact number'}))

  class Meta:
    model = User
    fields = ('first_name', 'last_name', 'username', 'phone_no', 'profile_pic',)


class StudentForm(forms.ModelForm):
  class Meta:
    model = Student
    exclude = ('user',)


class FacultyForm(forms.ModelForm):
  class Meta:
    model = Faculty
    exclude = ('user',)


class LibrarianForm(forms.ModelForm):
  class Meta:
    model = Librarian
    exclude = ('user',)


class UserLoginForm(forms.Form):
  username = forms.CharField(widget=forms.TextInput(attrs={'placeholder':'Enter your username'}))
  password = forms.CharField(widget=forms.PasswordInput(attrs={'placeholder':'Enter your password'}))

class AdminLoginForm(forms.Form):
  username = forms.CharField(widget=forms.TextInput(attrs={'placeholder':'Enter your username'}))
  password = forms.CharField(widget=forms.PasswordInput(attrs={'placeholder':'Enter your password'}))


class BookForm(forms.ModelForm):

  title = forms.CharField(widget=forms.TextInput(attrs={'placeholder':"Enter the title of the book"}))
  author = forms.CharField(widget=forms.TextInput(attrs={'placeholder':"Enter the author of the book"}))
  description = forms.CharField(widget=forms.Textarea(attrs={'placeholder':"Enter the description of the book"}))
  # no_of_copy = forms.IntegerField(widget=forms.NumberInput(attrs={'placeholder':"No of copies of books"}))
  # available_copy = forms.IntegerField(widget=forms.NumberInput(attrs={'placeholder':"Available copy of the book"}))
  cover_pic = forms.ImageField(label='Cover photo')

  class Meta:
    model = Book
    fields = '__all__'


class ContactForm(forms.Form):
  Email = forms.EmailField(widget=forms.EmailInput(attrs={'placeholder': 'Please enter your email'}))

  def __str__(self):
    return self.Email