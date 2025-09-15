from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from Shop import views


urlpatterns = [
    path('', views.ProductView.as_view(), name="home"),
    path('product/<int:pk>', views.ProductDetailsView.as_view(), name= 'show_product_details'),
    path('lehenga/', views.lehenga, name= 'lehengasingle'),
    path('lehenga/<slug:data>', views.lehenga, name= 'lehengaitems')
    
] + static(settings.MEDIA_URL, document_root = settings.MEDIA_ROOT)