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
  path('booklists/', views.BookLists.as_view(), name='book_lists'),
  path('addbook/', views.AddBook.as_view(), name='add_books'),  
  path('bookprofile/<int:pk>/', views.BookView.as_view(), name='book_profile'),
  path('bookupdate/<int:pk>/', views.BookUpdate.as_view(), name='book_update'),
  path('bookdelete/<int:pk>/', views.BookDelete.as_view(), name='book_delete'),
  path('adminhome/', views.AdminHome.as_view(), name='admin_home'), 
  
  path('studentlists/', views.StudentLists.as_view(), name='student_lists'),  
  path('facultylists/', views.FacultyLists.as_view(), name='faculty_lists'), 
  path('librarianlists/', views.LibrarianLists.as_view(), name='librarian_lists'), 

  path('user_update/<str:pk>/',views.UserUpdate.as_view(),name='user_update'),

  path('userdelete/<int:pk>/', views.UserDelete.as_view(), name='user_delete'),

  path('contact/', views.ContactView.as_view(), name='contact_us'),
  path('validate_username/', views.ValidateUsername.as_view(), name='validate_username'),
  path('copy_incdec/', views.CopyIncDec.as_view(), name='copy_incdec'),

  path('book_records/', views.BookRecords.as_view(), name='book_records'),
  path('book_issue/', views.BookIssue.as_view(), name='book_issue'),
  path('user_book_issue/<int:pk>/' ,views.UserBookIssue.as_view(), name='user_book_issue'),
  path('user_book_return/<int:id>/' ,views.UserBookReturn.as_view(), name='user_book_return'),
  path('search_book/',views.BookSearch.as_view(), name='search_book'),

] 


