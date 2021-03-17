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
from django.db.models import Q
import datetime

from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

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



@method_decorator(login_required, name='dispatch')
class HomeView(View):
  def get(self, request):
    book_list = Book.objects.all().order_by('id')
    paginator = Paginator(book_list, 6)
    page_number = request.GET.get('page',1)   #page number
    try:
      books = paginator.page(page_number)
    except PageNotAnInteger:
      books = paginator.page(1)       # if page is not an integer deliver the past page means landing page
    except EmptyPage: 
      books = paginator.page(paginator.num_pages)  # if page is out of range deliver last page of results 
    return render(request, 'library/home.html', {'books':books})


class SignupView(View):
  def get(self, request):
    userform = UserForm()
    studentform = StudentForm()
    facultyform = FacultyForm()
    return render(request, 'library/signup.html', {'userform':userform, 'studentform':studentform, 'facultyform':facultyform})


  def post(self, request):
    studentform = StudentForm()
    facultyform = FacultyForm()

    user_role = {
            '1': StudentForm(request.POST),
            '2': FacultyForm(request.POST),
          }
        
    temp_role = request.POST.get('role')
    usertype = user_role.get(temp_role)
    userform = UserForm(request.POST, request.FILES)

    if userform.is_valid() and usertype.is_valid():
      subject = 'Welcome to Library Management System.'
      message = 'Thanks for Signing In! Hope you will enjoy our services!!'
      recepient = str(userform['email'].value())
      send_mail(subject, message, EMAIL_HOST_USER, [recepient], fail_silently=False)

      user = userform.save(commit=False)
      user.save()

      new_user = usertype.save(commit=False)
      new_user.user = user
      new_user.save()

      # login user
      login(request, user)
      return redirect('library:user_profile', pk=user.id)

    else:
      return render(request, 'library/signup.html', {'userform':userform, 'studentform':studentform, 'facultyform':facultyform})

    



class LibrarianSignup(View):
  def get(self, request):
    userform = UserForm()
    librarianform = LibrarianForm()
    return render(request, 'library/signup_librarian.html', {'userform':userform, 'librarianform':librarianform})
  

  def post(self, request):
    userform = UserForm(request.POST, request.FILES)
    librarianform = LibrarianForm(request.POST)

    if userform.is_valid() and librarianform.is_valid():
      subject = 'Welcome to Online Library Management System'
      message = 'Hope you are enjoying!!'
      recepient = str(userform['email'].value())
      send_mail(subject, message, EMAIL_HOST_USER, [recepient], fail_silently=False)

      user = userform.save(commit=False)

      role1 = Role.objects.get(role='Librarian')
      user.role = role1

      user.save()
      librarian = librarianform.save(commit=False)
      librarian.user = user
      librarian.save()

      login(request, user)
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



# Admin Part Book CRUD
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
    return render(request, 'library/edit_books.html', {'bookform':bookform, 'books':book})


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
  paginate_by = 10


@method_decorator(staff_member_required, name='dispatch')
class FacultyLists(ListView):
  queryset = Faculty.objects.all().order_by('id')
  template_name = 'library/faculty_lists.html'
  context_object_name = "faculty"
  paginate_by = 10


@method_decorator(staff_member_required, name='dispatch')
class LibrarianLists(ListView):
  queryset = Librarian.objects.all().order_by('id')
  template_name = 'library/librarian_lists.html'
  context_object_name = "librarian"
  paginate_by = 10



class UserUpdate(LoginRequiredMixin, View):
    login_url = '/login/'

    def get(self,request,pk):
        user = User.objects.get(id=pk)
        userform = UserFormOne(instance=user)

        return render(request,'library/update.html',{'userform': userform,})

    def post(self,request,pk):
        user = User.objects.get(id=pk)
        userform = UserFormOne(request.POST, request.FILES, instance=user)

        if userform.is_valid():
          user1 = userform.save(commit=False)
          user1.save()
          messages.success(request,'User Updated Successfully')
          return redirect('library:user_update',pk=user1.id)

        else:
            return render(request,'library/signin.html',{'userform':userform})


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


class ValidateUsername(View):
  def post(self, request):
    username = request.POST.get('username', None)
    data = {
      'is_taken': User.objects.filter(username__iexact=username).exists()
    }
    return JsonResponse(data)


class ValidateEmail(View):
  def post(self, request):
    email = request.POST.get('email', None)
    data = {
      'is_taken': User.objects.filter(email__iexact=email).exists()
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



# Book Issue
class BookRecords(ListView):
  queryset = BookRecord.objects.all().order_by('id')
  template_name = 'library/book_records.html'
  context_object_name = "books"
  paginate_by = 10


@method_decorator(login_required, name='dispatch')
class BookIssue(View):
  def post(self, request):
    pk_user = request.POST.get('user_id')
    pk_book = request.POST.get('book_id')

    user = User.objects.get(id=pk_user)
    book = Book.objects.get(id=pk_book)

    # getting all the records from BookRecord for requested book
    all_book_records = BookRecord.objects.filter(book__title__iexact=book.title)

    # check if currentuser with requested book is already in BookRecords or not
    # or check if book title is occupied by another user
    for cur_user in all_book_records:
      if cur_user.user.username == user.username and cur_user.return_date == None:
        print("Book Already Issued")
        return JsonResponse({'status':0, 'msg':'Book Already Issued by You'})
    
    # getting all the user records from BookRecord for current user
    all_user_records = BookRecord.objects.filter(Q(user__username__iexact=user.username) & Q(return_date=None))

    # check if current user has issued book more than 3
    if all_user_records.count() > 2:
      print("Cannot issue book more than 3")
      return JsonResponse({'status':2, 'msg':'You cannot Issue book more than 3!!'})

    record = BookRecord.objects.create(book=book,user=user)
    record.book_due_date()
    record.save()
    book.available_copy -= 1
    book.save()

    return JsonResponse({'avail':book.available_copy})


@method_decorator(login_required, name='dispatch')
class UserBookIssue(View):
  def get(self, request, pk):
    user = User.objects.get(id=pk)
    books_issued = BookRecord.objects.filter(Q(user__username__iexact=user.username) & Q(return_date=None))
    return render(request, 'library/user_bookissue.html', {'user':user, 'books_issued':books_issued})


@method_decorator(login_required, name='dispatch')
class UserBookReturn(View):
  def get(self, request, id):
    current_book = BookRecord.objects.get(id=id)
    current_book.return_date = datetime.datetime.now()
    current_book.save()

    mybook = Book.objects.get(title=current_book.book.title)

    mybook.available_copy += 1
    mybook.save()
    messages.info(request, "Book returned successfully!!")

    return HttpResponseRedirect('/home')



@method_decorator(login_required, name='dispatch')
class BookSearch(View):
  def get(self, request):
    title = request.GET.get('search_book')
    book = Book.objects.filter(title__icontains=title)
    # print(book)
    return render(request,'library/book_search.html',{'books':book})


class AutoCompleteView(View):
  def get(self, request):
    if 'term' in request.GET:
      queryset = BookRecord.objects.filter(book__title__icontains=request.GET.get('term'))
      # print(queryset)
      titles = list()

      for book in queryset:
        titles.append(book.book.title)

      return JsonResponse(titles, safe=False)


class RecordSearch(LoginRequiredMixin, View):
  login_url = '/login/'

  def get(self, request):
    title = request.GET.get('title')
    book_record = BookRecord.objects.filter(book__title__icontains=title)
    # print(len(book_record))
    record_search = []

    for record in book_record:
      details = {
        'id':record.id,
        'title':record.book.title,
        'user':record.user.username,
        'issue_date':record.issue_date,
        'due_date':record.due_date,
        'return_date':record.return_date,
      }
      record_search.append(details)

      # print(record_search)

    return JsonResponse({'records':record_search})

