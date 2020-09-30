from django.urls import path

from .views import (

	product,
	customer,
	dashboard,
	CreateOrder,
	UpdateOrder,
	DeleteOrder,
	RegisterPage,
	LoginPage,
	LogoutPage,
	UserPage,
	AccountSettings,
	)

from django.contrib.auth import views as auth_views



app_name = 'accounts'
urlpatterns = [
	path('register/', RegisterPage, name='register'),
	path('login/', LoginPage, name='login'),
	path('logout/', LogoutPage, name='logout'),
	path('user/', UserPage, name='user'),


	path('account/', AccountSettings, name='settings'),


	path('', dashboard, name='home'),
	path('product/', product, name='products'),
	path('customer/<str:pk>/', customer, name='customers'),


	path('create_order/<str:pk>/', CreateOrder, name='create_order'),
	path('update_order/<str:pk>/', UpdateOrder, name='update_order'),
	path('delete_order/<str:pk>/', DeleteOrder, name='delete_order'),


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