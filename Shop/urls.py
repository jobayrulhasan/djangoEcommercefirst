from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from Shop import views


urlpatterns = [
    path('', views.ProductView.as_view(), name="home"),
    
] + static(settings.MEDIA_URL, document_root = settings.MEDIA_ROOT)