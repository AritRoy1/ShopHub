from django.shortcuts import render, redirect
from django.http import HttpResponse , HttpResponseRedirect 
from .models import Customer, Vendor, MultipleAddress
from .forms import CustomerRegistrationForm, VendorRegistrationForm
from django.views import View
from django.contrib.auth import authenticate, login , logout
from .forms import LoginForm, CustomerProfileForm, AddAddressForm
from django. contrib import messages
from product.models import Category, Image, Product, SubCategory



def home(request):
    category = Category.objects.all()
    subcatagory = SubCategory.objects.all()   
    image = Image.objects.all()
    # image1 = Image.objects.filter()
    
    dict1={}
    dict2={}
    for item in category:

        dict1[item.name]=SubCategory.objects.filter(category__name = item.name)    
    
    for sub in subcatagory:
        dict2[sub.name]=Image.objects.filter(product__sub__name=sub.name)
    print(dict2)
    
    return render(request, 'customer/home.html', {'category':category, "dict1":dict1, "dict2":dict2,  'image':image, 'subactegory':subcatagory})

def CustomerRegistration(request):
    if request.method == "POST":
        form = CustomerRegistrationForm(request.POST)
        # form = CustomerRegistrationForm(request.POST) 
        if form.is_valid(): 
            form.save()
            return HttpResponseRedirect('/login/')
                 
    else:    
        form = CustomerRegistrationForm()
    return render(request, 'customer/customer.html', {"form":form})

def VendorRegistration(request):
    if request.method == "POST":
        form = VendorRegistrationForm(request.POST, request.FILES)
        # form = CustomerRegistrationForm(request.POST)
        if form.is_valid():
            
            form.save()
            return HttpResponseRedirect('/product/registration/')
        
      
    else:
          
        form = VendorRegistrationForm()
    return render(request, 'customer/vendor.html', {"form":form})


class Login(View):
    def get(self, request):
        form =LoginForm
        return render(request, 'customer/login.html', {"form":form})
    def post(self, request):
        form =LoginForm(request.POST)      
        if form.is_valid():
            username = request.POST["username"]
            password = request.POST["password"]
        
            User = authenticate(request, username=username, password=password)  
            
            if User is not None:
                login(request, User)
                
                return HttpResponseRedirect('/home/')      
            else:
                messages.info(request, 'username or password is wrong')

        else :
          return HttpResponse("dfghjk")
      
    
def logout_view(request):
    logout(request)
    return HttpResponseRedirect('/login/')
       
        
class ProductList(View):
    def get(self, request, pk):
        
        category = Category.objects.all()
        subcatagory = SubCategory.objects.get(pk=pk)
        phone = Product.objects.filter(id=1)
        category = Category.objects.all()
        img = Image.objects.filter(product__sub__id=pk)
        dict1={}
        
        for item in category:

            dict1[item.name]=SubCategory.objects.filter(category__name = item.name)

        return render(request, 'customer/list_product.html', {'dict1':dict1, 'subcatagory':subcatagory, "img":img,})
        
        
        # return render(request, 'customer/list_product.html', {'dict1':dict1,
        #                 "phone":phone, "img":img, 'category':category, 'subcatagory':subcatagory})


class ProductDetail(View):
    def get(self, request, pk):
        category = Category.objects.all()
        dict1={}
        for item in category:
            dict1[item.name]=SubCategory.objects.filter(category__name = item.name)
            
        print(pk)   
        
        phone = Product.objects.filter(id=pk)
        
        img = Image.objects.get(pk=pk)
        return render(request, 'customer/product_detail.html', {"phone":phone,
                "img":img, 'category':category, 'dict1':dict1})


class CustomerProfile(View):
    category = Category.objects.all()
    dict1={}
    for item in category:
        dict1[item.name]=SubCategory.objects.filter(category__name = item.name)
        
    def get(self, request):
       
        customer_data = Customer.objects.get(username = request.user)
        print(customer_data)
        form =CustomerProfileForm(instance=request.user.customer)
       
        return render(request, 'customer/profile.html', {'form':form, 'dict1':self.dict1})
    
    def post(self, request):
        form = CustomerProfileForm(request.POST, instance=request.user.customer)
        
        print("jjjj ")
        if form.is_valid():
            print("XXXXXX")
            form.save()
            return redirect('/profile/')
    
        # return render(request, 'customer/profile.html', {"dict1":self.dict1})


def address(request):
        print(request.user)
        address = MultipleAddress.objects.filter(customer__username = request.user) 
        print(address) 
        if address:   
             return render(request, 'customer/address.html', {'address':address} )
         
        else:
            return render(request, 'customer/address.html')
                   
    
        
class  AddAddress(View):
   
    def get(self, request):
        print(request.user)
        form =AddAddressForm()  
        return render(request, 'customer/add_address.html', {'form':form})
       
    def post(self , request):
        print("kjhgf")
        user = request.user
        print(user)
        form = AddAddressForm(request.POST)
        print(form)
  
        if form.is_valid():
            name = form.cleaned_data['name']
            phone_number = form.cleaned_data['phone_number']
            pincode = form.cleaned_data['pincode']
            locality = form.cleaned_data['locality']
            address = form.cleaned_data['address']
            city = form.cleaned_data['city']
            state = form.cleaned_data['name']
            landmark = form.cleaned_data['landmark']
            
            customer = Customer.objects.get(username = request.user)
            
            model = MultipleAddress(customer=customer, name=name, phone_number=phone_number,pincode=pincode, locality=locality, address=address, city=city, state=state, landmark=landmark)
            
            model.save()
            
            return redirect('/address/')
            
            
            
            

       