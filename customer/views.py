from django.shortcuts import render, redirect
from django.http import HttpResponseRedirect
from .models import Customer, Vendor, MultipleAddress
from .forms import CustomerRegistrationForm
from django.views import View
from django.contrib.auth import authenticate, login, logout
from .forms import LoginForm, CustomerProfileForm, AddAddressForm
from product.models import Category, Image, Product, SubCategory, Wishlist
from django.http import JsonResponse
from django.shortcuts import get_object_or_404
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator

# import ratting for product_detail
from ratting.models import Ratting


def home(request):
    # before pagination  
    # category = Category.objects.all()
    # subcatagory = SubCategory.objects.all()   
    # image = Image.objects.all()
       
    # dict1={}
    # dict2={}
    # for item in category:

    #     dict1[item.name]=SubCategory.objects.filter(category__name=item.name)  
    
    # for sub in subcatagory:
    #     dict2[sub.name]=Image.objects.filter(product__sub__name=sub.name)
        
    
    # return render(request, 'customer/home.html', {'category':category, "dict1":dict1, "dict2":dict2,  'image':image, 'subactegory':subcatagory,})


    # after pagination
    product = Product.objects.all()
    category = Category.objects.all()
    subcatagory = SubCategory.objects.all()
    image = Image.objects.all()
    dict_category = {}
    dict_subcategory = {}
    for item in category:
        dict_category[item.name] = SubCategory.objects.filter(category__name=item.name)   
    for sub in subcatagory:
        dict_subcategory[sub.name] = Image.objects.filter(product__sub__name=sub.name)     
    dict_list = list(dict_subcategory.items())
    paginator = Paginator(dict_list, 3, orphans=1)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    context = {
        'category': category,
        "dict1": dict_category,
        "dict2": dict_subcategory,
        'image': image,
        'subactegory': subcatagory,
        "page_obj": page_obj,
        "product": product 
    }
    return render(request, 'customer/home.html', context)


def CustomerRegistration(request):
    if request.method == "POST":
        form = CustomerRegistrationForm(request.POST)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect('/login/')           
    else:
        form = CustomerRegistrationForm()
        context = {
            "form": form
            
        }
    return render(request, 'customer/customer_registration.html', context)

## login form 

# class Login(View):
#     def get(self, request):    
#         form =LoginForm
#         return render(request, 'customer/login.html', {"form":form})
#     def post(self, request):     
#         form =LoginForm(request.POST)      
#         if form.is_valid():
#             username = request.POST["username"]
#             password = request.POST["password"]    
#             user = authenticate(request, username=username, password=password)  
            
#             if user is not None:
#                 login(request, user)
#                 print(request.user)
#                 if Vendor.objects.filter(username=request.user):
#                     return HttpResponseRedirect('/product/vendor-pannel/')
#                 else:   
#                     return HttpResponseRedirect('/home/')      
#             else:
#                 # messages.info(request, 'username or password is wrong')
#                 context={
#                     "form":form,
#                     'message':"username password not match",
#                 }
#                 return render(request, 'customer/login.html',context)
                

#         else :
#           return HttpResponse("form not valid")

    ##--------------->>>>>>>>>>>>>>>
    
## updated login form
class Login(View):
    def get(self, request):    
        form =LoginForm
        return render(request, 'customer/login.html', {"form":form})
    def post(self, request):
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user is not None:
                login(request, user)
                if Vendor.objects.filter(username=request.user):
                    return HttpResponseRedirect('/product/vendor-pannel/')
                else:   
                    return HttpResponseRedirect('/home/')      
        else:
            context={     
                    'message':"username password not match",
                }
            return render(request, 'customer/login.html',context)
              
# logout view
def logout_view(request):
    logout(request)
    return HttpResponseRedirect('/login/')

# after click show more it show another 5 review
def show_more_review(request):  
      page = request.GET.get('page')
      prod_id =  request.GET.get('prod_id')  
      page = int(page)
      reviews = Ratting.objects.filter(product__id=prod_id).order_by('-id')[5 * (page - 1):5 * page]  
      data = {
         'reviews': [{'text': review.comments} for review in reviews],
            }
      return JsonResponse(data)
  
# customer can see their own profile
class CustomerProfile(View):
    category = Category.objects.all()
    dict_category = {}
    for item in category:
        dict_category[item.name] = SubCategory.objects.filter(category__name = item.name)
        
    def get(self, request):    
        customer_data = Customer.objects.get(username = request.user)
        form =CustomerProfileForm(instance=request.user.customer) 
        context = {
            'form': form, 
            'dict1': self.dict_category
            } 
        return render(request, 'customer/customer_profile.html', context)
    
    def post(self, request):
        form = CustomerProfileForm(request.POST, instance=request.user.customer)      
        if form.is_valid():      
            form.save()
            return redirect('/profile/')
        
        
# customer can see their address      
def show_address(request):      
        address = MultipleAddress.objects.filter(customer__username = request.user)    
        if address:   
             return render(request, 'customer/customer_show_address.html', {'address':address} )
         
        else:
            return render(request, 'customer/customer_show_address.html')

# customer can add their multiple address     
class  AddAddress(View):
    def get(self, request):
        form =AddAddressForm()  
        return render(request, 'customer/customer_add_address.html', {'form':form})
       
    def post(self , request): 
        form = AddAddressForm(request.POST)   
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
              
            # save multiple address of one customer  
            model = MultipleAddress(customer=customer, name=name, phone_number=phone_number,pincode=pincode, locality=locality, address=address, city=city, state=state, landmark=landmark)   
            model.save()     
            return redirect('/address/')


# customer can delete address 
def delete_address(request, pk):
    address = MultipleAddress(pk=pk)
    address.delete()
    return redirect('/address/')  

def wishlist(request):
    wishlist = Wishlist.objects.filter(customer__username = request.user)
    return render(request, 'customer/wishlist.html', {"wishlist":wishlist})

                                 
def add_to_wishlist(request, product_id): 
    image = get_object_or_404(Image, id=product_id)  
    product = Product.objects.get(image__id=product_id)
    user = Customer.objects.get(username=request.user)    
    if not Wishlist.objects.filter(customer=user, product=product, image=image).exists():
        wishlist_item = Wishlist(customer=user, product=product, image=image)        
        wishlist_item.save()
        return JsonResponse({'message': 'Item added to wishlist'})
    return JsonResponse({'message': 'Item is already in the wishlist'})


def remove_from_wishlist(request, product_id):
    image = get_object_or_404(Image, id=product_id)
    product=Product.objects.get(image__id=product_id)  
    user = Customer.objects.get(username=request.user)
    try:
        wishlist_item = Wishlist.objects.get(customer=user, product=product, image=image)
        wishlist_item.delete()
        return JsonResponse({'message': 'Item removed from wishlist'})
    except Wishlist.DoesNotExist:
        return JsonResponse({'message': 'Item was not in the wishlist'})
    
    
