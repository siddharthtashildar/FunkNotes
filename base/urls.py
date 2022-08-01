from django.urls import path
from . import views
from django.contrib.auth import views as auth_views

urlpatterns = [

    path('',views.home, name='home'),

    path('login/', views.loginUser, name="login"),
    path('logout/', views.logoutUser, name="logout"),
    path('register/', views.registerUser, name="register"),

    path('settings/',views.Settings,name="settings"),
    path('verify_pass/',views.verify_pass,name="veri_pass"),
    path('change_password/',views.Edit_password,name='ChangePassword'),
    path('delete_account/',views.delete_account,name="deleteAccount"),

    path('notes/', views.noteslist , name='notes'),
    path('note/<str:pk>/',views.Note,name='note'),
    path('create/',views.Create_note,name='create'),
    path('edit/<str:pk>/',views.Edit_note,name='edit'),
    path('delete/<str:pk>',views.Delete_note,name='delete'),

    path('reset_password/',
     auth_views.PasswordResetView.as_view(template_name="password_reset.html"),
     name="reset_password"),

    path('reset_password_sent/', 
        auth_views.PasswordResetDoneView.as_view(template_name="password_reset_sent.html"), 
        name="password_reset_done"),

    path('reset/<uidb64>/<token>/',
     auth_views.PasswordResetConfirmView.as_view(template_name="password_reset_form.html"), 
     name="password_reset_confirm"),

    path('reset_password_complete/', 
        auth_views.PasswordResetCompleteView.as_view(template_name="password_reset_done.html"), 
        name="password_reset_complete"),
]