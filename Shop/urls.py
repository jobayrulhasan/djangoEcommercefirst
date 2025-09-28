from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from Shop import views
from django.contrib.auth import views as auth_views
from .forms import MyPasswordChangeForm, MyPasswordResetForm, MySetPasswordForm


urlpatterns = [
    path('', views.ProductView.as_view(), name="home"),
    path('product/<int:pk>', views.ProductDetailsView.as_view(), name= 'show_product_details'),
    #Add to cart
    path('addcart/', views.add_to_cart, name='addtocart'),
    # lehenga
    path('lehenga/', views.lehenga, name= 'lehengasingle'),
    path('lehenga/<slug:data>', views.lehenga, name= 'lehengaitems'),
    #sharee
    path('sharee/', views.sharee, name= 'shareesingle'),
    path('sharee/<slug:data>', views.sharee, name= 'shareeitems'),
    
    # customer registration
    path('registration/', views.CustomerRegistrationView.as_view(), name='userregistration'),
    # login
    path('accounts/login/', views.user_login, name='loginpage'),
    # logout
    path('account/logout/', views.user_logout, name='userLogout'),
    
    # change password
    path('passwordchange/', auth_views.PasswordChangeView.as_view(template_name ='Shop/passwordchange.html', form_class=MyPasswordChangeForm, success_url='/passwordchangedone/'), name="passwordchange"),
    path('passwordchangedone/', auth_views.PasswordChangeView.as_view(template_name='Shop/passwordchangedone.html'), name="passwordchangedone"),
    
    # password rest. This four (password reset, reset done, reset confirm and reset complete) is mendatory for reset password in django 5.2 version
    path('password_reset', auth_views.PasswordResetView.as_view(template_name="Shop/password_reset.html", form_class=MyPasswordResetForm), name='password_reset'),
    path('password_reset/done/', auth_views.PasswordResetDoneView.as_view(template_name='Shop/password_reset_done.html'), name='password_reset_done'),
    path('password_reset_confirm/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(template_name='Shop/password_reset_confirm.html', form_class=MySetPasswordForm), name='password_reset_confirm'),
    path('password_reset_complete/', auth_views.PasswordResetCompleteView.as_view(template_name='Shop/password_reset_complete.html'), name='password_reset_complete'),

    # profile
    path('profile/', views.ProfileView.as_view(), name='profilepage'),
    # Address
     path('address/', views.address, name='address'),
    
] + static(settings.MEDIA_URL, document_root = settings.MEDIA_ROOT)