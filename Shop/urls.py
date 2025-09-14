from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from Shop import views


urlpatterns = [
    path('', views.ProductView.as_view(), name="home"),
    path('product/<int:pk>', views.ProductDetailsView.as_view(), name= 'show-product-details')
    
] + static(settings.MEDIA_URL, document_root = settings.MEDIA_ROOT)