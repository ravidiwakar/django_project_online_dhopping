from django.urls import path,include
from django.conf import settings
from django.conf.urls.static import static
from app import views
from app.views import CustomerRegistrationView
from .forms import LoginForm, MyPasswordChangeForm,MyPasswordResetForm,MySetPasswordForm
from django.contrib.auth import views as auth_views
urlpatterns = [
    path('', views.ProductView.as_view(), name="home"),
    path('product-detail/<int:pk>', views.product_detail, name='product-detail'),
    # path('product-detail/<int:pk>', ProductDetailView.as_view(), name='product-detail'),
    path('add-to-cart/', views.add_to_cart, name='add-to-cart'),
    path('show-cart/', views.show_cart, name='show-cart'),
    path('pluscart/', views.plus_cart),
    path('minuscart/', views.minus_cart),
    path('removecart/', views.remove_cart),
    path('checkout/', views.checkout, name='checkout'),
    path('paymentdone/', views.payment_done, name='paymentdone'),
    # path('remove-cart/(?P<part_id>[0-9]+)/$', views.remove_cart, name='remove-cart'),
    # path('remove-cart/', views.remove_cart, name='remove-cart'),
    # path('cart/<str:id>/delete/', views.deletecart, name='deletecart'),
    path('buy/', views.buy_now, name='buy-now'),
    path('profile/', views.CustomerProfileView.as_view(), name='profile'),
    path('address/', views.address, name='address'),
    path('orders/', views.orders, name='orders'),
    # path('changepassword/', views.change_password, name='changepassword'),
    # path('passwordreset/', views.password_reset, name='passwordreset'),
    path('mobile/', views.mobile, name='mobile'),
    path('mobile/<slug:data>', views.mobile, name='mobiledata'),
    # path('login/', views.login, name='login'),
    path('accounts/login/', auth_views.LoginView.as_view(template_name='app/login.html', authentication_form=LoginForm), name='login'),
    path('logout/', auth_views.LogoutView.as_view(next_page="login"), name='logout'),
    path('passwordchange/', auth_views.PasswordChangeView.as_view(template_name='app/passwordchange.html', form_class=MyPasswordChangeForm), name='passwordchange'),
    path('password_change/done/', auth_views.PasswordChangeDoneView.as_view(template_name='app/password_change_done.html'), name='password_change_done'),
    path('password_reset', auth_views.PasswordResetView.as_view(template_name='app/passwordreset.html', form_class=MyPasswordResetForm), name='passwordreset'),
    path('password_reset/done/', auth_views.PasswordResetDoneView.as_view(template_name='app/password_reset_done.html'), name='password_reset_done'),
    path('password_reset_confirm/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(template_name='app/password_reset_confirm.html', form_class=MySetPasswordForm), name='password_reset_confirm'),
    path('password_reset_complete/done/', auth_views.PasswordResetCompleteView.as_view(template_name='app/password_reset_complete.html'), name='password_reset_complete'),
    path('registration/', views.CustomerRegistrationView.as_view(), name='customerregistration'),
    
    # path('registration/', views.CustomerRegistrationView.as_view(), name='customerregistration')
]   + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
