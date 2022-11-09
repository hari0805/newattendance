from django.urls import path

from django.contrib.auth import views as auth_views

from . import views



urlpatterns = [
	path('register/', views.registerPage, name="register"),
	path('login/', views.loginPage, name="login"),  
	path('logout/', views.logoutUser, name="logout"),

    path('home', views.home, name="home"),
    path('', views.clockin_clockout, name="attendance"),

    path('leave/', views.leave_application, name="leave_application"),
    # path('leave_app', views.contact, name="send_mail"),

    # path('leave/thanks/', views.greet_mail, name="greet_mail"),

    path('account/', views.accountSettings, name="account"),
    path('pdf/', views.DownloadPdf, name='DownloadPdf'),

    path('detail_view/<str:pk>/', views.detail_view, name="detail_view"),
    path('delete_view/<str:pk>/', views.delete_emp, name="delete_view"),

    path('reset_password/',
     auth_views.PasswordResetView.as_view(template_name="accounts/password_reset.html"),
     name="reset_password"),

    path('reset_password_sent/', 
        auth_views.PasswordResetDoneView.as_view(template_name="accounts/password_reset_sent.html"), 
        name="password_reset_done"),

    path('reset/<uidb64>/<token>/',
     auth_views.PasswordResetConfirmView.as_view(template_name="accounts/password_reset_form.html"), 
     name="password_reset_confirm"),

    path('reset_password_complete/', 
        auth_views.PasswordResetCompleteView.as_view(template_name="accounts/password_reset_done.html"), 
        name="password_reset_complete"),



]

'''
1 - Submit email form                         //PasswordResetView.as_view()
2 - Email sent success message                //PasswordResetDoneView.as_view()
3 - Link to password Rest form in email       //PasswordResetConfirmView.as_view()
4 - Password successfully changed message     //PasswordResetCompleteView.as_view()
'''