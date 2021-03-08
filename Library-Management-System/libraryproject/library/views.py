from django.shortcuts import render, redirect
from django.views import View
from library.forms import *
from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.contrib import messages
from library.models import *
from django.contrib.admin.views.decorators import staff_member_required
from django.contrib.auth.mixins import LoginRequiredMixin

# Create your views here.
@method_decorator(staff_member_required, name='dispatch')
class BookListsView(View):
  def get(self, request):
    book = Book.objects.all()
    return render(request, 'library/book_lists.html',{'books':book})


@method_decorator(login_required, name='dispatch')
class HomeView(View):
  def get(self, request):
    return render(request, 'library/home.html')


class SignupView(View):
  def get(self, request):
    userform = UserForm()
    studentform = StudentForm()
    facultyform = FacultyForm()
    deptform = DepartmentForm()
    roleform = RoleForm()
    return render(request, 'library/signup.html', {'userform':userform, 'studentform':studentform, 'departmentform':deptform, 'roleform':roleform, 'facultyform':facultyform})


  def post(self, request):
    user_role = {
            'Student': StudentForm(request.POST),
            'Faculty': FacultyForm(request.POST),
          }
        
    roleform = RoleForm(request.POST)
        
    if roleform.is_valid():
      temp_role = roleform.cleaned_data['role']
      usertype = user_role.get(temp_role)
      
      userform = UserForm(request.POST, request.FILES)
      deptform = DepartmentForm(request.POST)

      if userform.is_valid() and usertype.is_valid() and deptform.is_valid() and roleform.is_valid():

        role = roleform.save(commit=False)   
        role1 = Role.objects.filter(role=role).first()
        # saving user with department
        user = userform.save(commit=False)

        # department and Role saved
        dept = deptform.save(commit=False)
        dept1 = Department.objects.filter(department=dept).first()
        user.department = dept1
    
        user.role = role1
        user.save()

        new_user = usertype.save(commit=False)
        new_user.user = user
        new_user.save()

        login_userr = authenticate(username=userform.cleaned_data['username'], password=userform.cleaned_data['password1'])
        login(request, login_userr)
        return redirect('library:user_profile', pk=user.id)

      else:
        return render(request, 'library/signup.html', {'userform': userform, 'departmentform':deptform, 'roleform':roleform})
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
    # print(self.uname, self.upass)
    self.user = authenticate(username=self.uname, password=self.upass)
    # print(self.user)

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
      # return redirect('library:book_profile', pk=book.id)
      return redirect('library:book_lists')

    else:
      return render(request, 'library/add_books.html', {'bookform':bookform, 'categoryform':categoryform})


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
    return render(request, 'library/add_books.html', {'bookform':bookform})

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
      return render(request, 'library/add_books.html', {'bookform':bookform})


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
class StudentLists(View):
  def get(self, request):
    student = Student.objects.all()
    return render(request, 'library/student_lists.html', {'students':student})

@method_decorator(staff_member_required, name='dispatch')
class FacultyLists(View):
  def get(self, request):
    faculty = Faculty.objects.all()
    return render(request, 'library/faculty_lists.html', {'faculty':faculty})


@method_decorator(staff_member_required, name='dispatch')
class LibrarianLists(View):
  def get(self, request):
    librarian = Librarian.objects.all()
    return render(request, 'library/librarian_lists.html', {'librarian':librarian})

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
class StudentDelete(View):
  def post(self, request, pk):
    student = User.objects.get(id=pk)
    student.delete()
    return redirect('library:student_lists')


@method_decorator(staff_member_required, name='dispatch')
class FacultyDelete(View):
  def post(self, request, pk):
    faculty = User.objects.get(id=pk)
    faculty.delete()
    return redirect('library:faculty_lists')


@method_decorator(staff_member_required, name='dispatch')
class LibrarianDelete(View):
  def post(self, request, pk):
    librarian = User.objects.get(id=pk)
    librarian.delete()
    return redirect('library:librarian_lists')