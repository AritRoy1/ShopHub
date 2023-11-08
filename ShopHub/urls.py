
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static 


urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('customer.urls')),
    path("product/", include('product.urls'), name='product'),
    path('payment/', include("payment.urls"), name="payment"),
    path('ratting/', include('ratting.urls')),

    
    # path('customer/registration', views.CustomerRegistration, name='customer-registration'),
    # path('vendor/registration', views.VendorRegistration, name = 'vendor')
        
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
