from django.urls import path
from library import views

app_name = 'library'

urlpatterns = [
  path('home/', views.HomeView.as_view(), name='home'),
  path('signup/', views.SignupView.as_view(), name='signup'),
  path('libsignup/', views.LibrarianSignup.as_view(), name='libsignup'),
  path('login/', views.LoginView.as_view(), name='userlogin'),
  path('logout/', views.LogoutView.as_view(), name='userlogout'),
  path('profile/<int:pk>/', views.UserProfileView.as_view(), name='user_profile'),
  path('booklists/', views.BookListsView.as_view(), name='book_lists'),
  path('addbook/', views.AddBook.as_view(), name='add_books'),  
  path('bookprofile/<int:pk>/', views.BookView.as_view(), name='book_profile'),
  path('bookupdate/<int:pk>/', views.BookUpdate.as_view(), name='book_update'),
  path('bookdelete/<int:pk>/', views.BookDelete.as_view(), name='book_delete'),
  path('adminhome/', views.AdminHome.as_view(), name='admin_home'), 
  path('studentlists/', views.StudentLists.as_view(), name='student_lists'),  
  path('facultylists/', views.FacultyLists.as_view(), name='faculty_lists'), 
  path('librarianlists/', views.LibrarianLists.as_view(), name='librarian_lists'), 
  
  path('studentedit/<int:pk>/', views.StudentEdit.as_view(), name='student_edit'),
  path('facultyedit/<int:pk>/', views.FacultyEdit.as_view(), name='faculty_edit'),
  path('librarianedit/<int:pk>/', views.LibrarianEdit.as_view(), name='librarian_edit'),
  path('userdelete/<int:pk>/', views.UserDelete.as_view(), name='user_delete'),



]


