from django.urls import path
from ratting import views
urlpatterns = [  
    path('submit/',views.ratting, name="ratting"),   
]