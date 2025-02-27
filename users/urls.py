from django.urls import path,include
from . import views
app_name='users'
urlpatterns = [
    path('register/', views.register_view, name='register'),
    path('login/', views.login_view, name='login'),
    path('', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('my-account/', views.my_account, name='my-account'),
    path('accounts_edit/', views.accounts_edit, name='accounts_edit'),
    path('forgot_password/', views.forgot_password, name='forgot_password'),
    path('restore_password/', views.restore_password, name='restore_password'),
]