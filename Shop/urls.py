from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from Shop import views


urlpatterns = [
    path('', views.ProductView.as_view(), name="home"),
    path('product/<int:pk>', views.ProductDetailsView.as_view(), name= 'show_product_details'),
    # lehenga
    path('lehenga/', views.lehenga, name= 'lehengasingle'),
    path('lehenga/<slug:data>', views.lehenga, name= 'lehengaitems'),
    #sharee
    path('sharee/', views.sharee, name= 'shareesingle'),
    path('sharee/<slug:data>', views.sharee, name= 'shareeitems'),
    # customer registration
    path('registration/', views.CustomerRegistrationView.as_view(), name='userregistration'),
    # login
    path('login/', views.user_login, name='loginpage')
    
] + static(settings.MEDIA_URL, document_root = settings.MEDIA_ROOT)