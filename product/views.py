from django.shortcuts import render
from django.views import View
from .forms import ProductForm
from django.http import HttpResponse

class ProductRegistration(View):
    def get(self, request):
        form =ProductForm
        return render(request, 'product/product.html', {"form":form})
    
    def post(self, request):
        form =ProductForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return HttpResponse("sucessfully Submited")