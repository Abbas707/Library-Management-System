from django.shortcuts import render, redirect
from django.views import View
from django.views.generic import ListView
from library.forms import *
from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.contrib import messages
from library.models import *
from django.contrib.admin.views.decorators import staff_member_required
from django.contrib.auth.mixins import LoginRequiredMixin
from libraryproject.settings import EMAIL_HOST_USER,EMAIL_HOST_PASSWORD
from django.http import JsonResponse
from django.core.mail import send_mail

# E-mail functionality
@method_decorator(login_required, name='dispatch')
class ContactView(View):
  def get(self, request):
    form = ContactForm()
    return render(request, 'library/contact.html',{'form':form})

  def post(self, request):
    form = ContactForm(request.POST)
    subject = 'Hi, Everyone'
    message = 'Hope you are enjoying in BoTree Technologies'
    recepient = str(form['Email'].value())
    send_mail(subject, message, EMAIL_HOST_USER, [recepient], fail_silently=False)
    messages.info(request, 'Email Sent successfully!!')

    return render(request, 'library/contact.html',{'form':form})


# Create your views here.
@method_decorator(login_required, name='dispatch')
class HomeView(ListView):
  queryset = Book.objects.all()[::-1]
  template_name = 'library/home.html'
  context_object_name = "books"
  paginate_by = 8


class SignupView(View):
  def get(self, request):
    userform = UserForm()
    studentform = StudentForm()
    facultyform = FacultyForm()
    return render(request, 'library/signup.html', {'userform':userform, 'studentform':studentform,'facultyform':facultyform})


  def post(self, request):
    user_role = {
            '1': StudentForm(request.POST),
            '2': FacultyForm(request.POST),
          }
        
    temp_role = request.POST.get('role')
    usertype = user_role.get(temp_role)
    userform = UserForm(request.POST, request.FILES)

    if userform.is_valid() and usertype.is_valid():
      user = userform.save(commit=False)
      user.save()

      new_user = usertype.save(commit=False)
      new_user.user = user
      new_user.save()

      # login user
      login(request, user)
      return redirect('library:user_profile', pk=user.id)

    else:
        return render(request, 'library/signup.html', {'userform': userform, 'departmentform':deptform, 'roleform':roleform})


class LibrarianSignup(View):
  def get(self, request):
    userform = UserForm()
    librarianform = LibrarianForm()

    return render(request, 'library/signup_librarian.html', {'userform':userform, 'librarianform':librarianform})
  

  def post(self, request):
    userform = UserForm(request.POST, request.FILES)
    librarianform = LibrarianForm(request.POST)

    if userform.is_valid() and librarianform.is_valid():
      user = userform.save(commit=False)

      role1 = Role.objects.filter(role='Librarian').first()
      user.role = role1

      user.save()
      librarian = librarianform.save(commit=False)
      librarian.user = user
      librarian.save()

      login_userr = authenticate(username=userform.cleaned_data['username'], password=userform.cleaned_data['password1'])
      login(request, login_userr)
      return redirect('library:user_profile', pk=user.id)

    else:
      return render(request, 'library/signup_librarian.html', {'userform':userform, 'librarianform':librarianform})



class LoginView(View):
  def get(self, request):
    form = UserLoginForm()
    return render(request, 'library/login.html', {'form':form})


  def post(self, request):
    self.uname = request.POST['username']
    self.upass = request.POST['password']

    self.user = authenticate(username=self.uname, password=self.upass)
  
    if self.user:
      if self.user.is_active:
        login(request, self.user)
        if self.user.is_staff:
          return redirect('library:admin_home')
        return redirect('library:user_profile', pk=self.user.id)
      else:
        return HttpResponse('Account not active')

    else:
      messages.error(request,'Invalid username or password!!')
      return redirect('library:userlogin')


class LogoutView(View):
  def get(self, request):
    logout(request)
    return redirect('library:userlogin')


class UserProfileView(LoginRequiredMixin,View):
  login_url = '/login/'

  def dispatch(self, *args, **kwargs):
    return super().dispatch(*args, **kwargs)

  def get(self, request, pk):
    user = User.objects.get(id=pk)
    return render(request, 'library/user_profile.html', {'user':user})



# Admin Part CRUD
@method_decorator(staff_member_required, name='dispatch')
class AddBook(View):
  def get(self, request):
    bookform = BookForm()
    return render(request, 'library/add_books.html', {'bookform':bookform})

  def post(self, request):
    bookform = BookForm(request.POST, request.FILES)

    if bookform.is_valid():
      book = bookform.save(commit=False)
      category = bookform.cleaned_data['category']
      new_category = Category.objects.get(category=category)
      book.category = new_category
      book.save()
      return redirect('library:book_lists')

    else:
      return render(request, 'library/add_books.html', {'bookform':bookform, 'categoryform':categoryform})


@method_decorator(staff_member_required, name='dispatch')
class BookLists(ListView):
  queryset = Book.objects.all().order_by('id')
  template_name = 'library/book_lists.html'
  context_object_name = "books"
  paginate_by = 5
  

@method_decorator(login_required, name='dispatch')
class BookView(View):
  def get(self, request, pk):
    book = Book.objects.get(id=pk)
    return render(request, 'library/book_profile.html', {'book':book})


@method_decorator(staff_member_required, name='dispatch')
class BookUpdate(View):
  def get(self, request, pk):
    book = Book.objects.get(id=pk)
    bookform = BookForm(instance=book)
    return render(request, 'library/edit_books.html', {'bookform':bookform,'books':book})


  def post(self, request, pk):
    book = Book.objects.get(id=pk)
    bookform = BookForm(request.POST, instance=book)

    if bookform.is_valid():
      book = bookform.save(commit=False)
      category = bookform.cleaned_data['category']
      new_category = Category.objects.get(category=category)

      book.category = new_category
      book.save()
      messages.info(request, "Book Updated sucessfully!!")
      return redirect('library:book_profile', pk=book.pk)
    
    else:
      return render(request, 'library/edit_books.html', {'bookform':bookform})


@method_decorator(staff_member_required, name='dispatch')
class BookDelete(View):
  def get(self, request, pk):
    book = Book.objects.get(id=pk)
    book.delete()
    return redirect('library:book_lists')



# Admin Dashboard
@method_decorator(staff_member_required, name='dispatch')
class AdminHome(View):
  def get(self, request):
    return render(request, 'library/admin_home.html')


@method_decorator(staff_member_required, name='dispatch')
class StudentLists(ListView):
  queryset = Student.objects.all()
  template_name = 'library/student_lists.html'
  ordering = ['id']
  context_object_name = "students"
  paginate_by = 2


@method_decorator(staff_member_required, name='dispatch')
class FacultyLists(ListView):
  queryset = Faculty.objects.all().order_by('id')
  template_name = 'library/faculty_lists.html'
  context_object_name = "faculty"
  paginate_by = 2


@method_decorator(staff_member_required, name='dispatch')
class LibrarianLists(ListView):
  queryset = Faculty.objects.all().order_by('id')
  template_name = 'library/librarian_lists.html'
  context_object_name = "librarian"
  paginate_by = 2



@method_decorator(staff_member_required, name='dispatch')
class StudentEdit(View):
  def get(self, request, pk):
    student = User.objects.get(id=pk)
    userform = UserFormOne(instance=student)
    return render(request, 'library/signup.html', {'userform': userform})

  def post(self, request, pk):
    student = User.objects.get(id=pk)
    userform = UserFormOne(request.POST, request.FILES, instance=student)
    
    if userform.is_valid():
      student = userform.save(commit=False)
      student.save()
      return redirect('library:student_lists')
    else:
      return redirect('library:student_edit', pk=student.pk)


@method_decorator(staff_member_required, name='dispatch')
class FacultyEdit(View):
  def get(self, request, pk):
    faculty = User.objects.get(id=pk)
    userform = UserFormOne(instance=faculty)
    return render(request, 'library/signup.html', {'userform': userform})

  def post(self, request, pk):
    faculty = User.objects.get(id=pk)
    userform = UserFormOne(request.POST, request.FILES, instance=faculty)
    
    if userform.is_valid():
      faculty = userform.save(commit=False)
      faculty.save()
      return redirect('library:faculty_lists')
    
    else:
      return redirect('library:faculty_edit', pk=faculty.pk)


@method_decorator(staff_member_required, name='dispatch')
class LibrarianEdit(View):
  def get(self, request, pk):
    librarian = User.objects.get(id=pk)
    userform = UserFormOne(instance=librarian)
    return render(request, 'library/signup.html', {'userform': userform})

  def post(self, request, pk):
    librarian = User.objects.get(id=pk)
    userform = UserFormOne(request.POST, request.FILES, instance=librarian)
    
    if userform.is_valid():
      librarian = userform.save(commit=False)
      librarian.save()
      return redirect('library:librarian_lists')
    
    else:
      return redirect('library:librarian_edit', pk=librarian.pk)


@method_decorator(staff_member_required, name='dispatch')
class UserDelete(View):
  def get(self, request, pk):
    user = User.objects.get(id=pk)
    new_role = user.role.role
    user.delete()

    if new_role == 'Student':
      return redirect('library:student_lists')
    elif new_role == 'Faculty':
      return redirect('library:faculty_lists')
    else:
      return redirect('library:librarian_lists')


class validate_username(View):
  def post(self, request):
    username = request.POST.get('username', None)
    data = {
      'is_taken': User.objects.filter(username__iexact=username).exists()
    }
    return JsonResponse(data)


class CopyIncDec(View):
  def post(self, request):
    pk = request.POST.get('id')
    symbol = request.POST.get('symbol')
    book = Book.objects.get(id=pk)

    if symbol == 'plus':
      book.no_of_copy += 1
      book.available_copy +=1
    else:
      book.no_of_copy -= 1
      book.available_copy -= 1

    book.save()
    return JsonResponse({'status':1, 'book_copy':book.no_of_copy, 'avail':book.available_copy})



