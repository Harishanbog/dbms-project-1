from django.http import response
from django.http.response import JsonResponse
from django.shortcuts import render,redirect,get_object_or_404
from django.views.generic import DetailView,ListView,View
from .models import BillingAddress, Category,Items,Order,OrderItem,TotalOrder, UserOtp
from .forms import AddressForm
from django.core.exceptions import ObjectDoesNotExist
from django.contrib.auth.decorators import login_required
from django.contrib.admin.views.decorators import staff_member_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.models import User,auth
from django.contrib import messages
from django.http import HttpResponse, request
from django.contrib.sites.shortcuts import get_current_site
from django.utils import timezone
from django.core.mail import send_mail
from django.urls import reverse
from django.template.loader import get_template
from xhtml2pdf import pisa
import csv
import datetime
import random
from bhavani import settings
from django.views.decorators.csrf import csrf_exempt

# Create your views here.
def homeview(request):
    if request.method=='POST':
        search_element=request.POST.get('product')
        items=Items.objects.filter(title=search_element)
        if search_element=='':
            items=Items.objects.all()
        categories=Category.objects.all()
        context={
            'object_list':items,
            'categories':categories
        }
        return render(request,"cart/home.html",context)
        
    else:        
        category=request.GET.get('category')
        if category=='none':
            items=Items.objects.all()
        else:
            items=Items.objects.filter(category__name=category)   

        if category is None:
            items=Items.objects.all()    

        #search
        if 'term' in request.GET:
            qs=Items.objects.filter(title__icontains=request.GET.get('term'))
            titles= list()
            for product in qs:
                titles.append(product.title)
            return JsonResponse(titles,safe=False)    
            
        categories=Category.objects.all()
        context = {
            'object_list':items,
            'categories':categories
        }    
        return render(request,"cart/home.html",context)
    



def Productsview(request):
    category=request.GET.get('category')
    if category=='none':
        items=Items.objects.all()
    else:
        items=Items.objects.filter(category__name=category)   

    if category is None:
        items=Items.objects.all()    
        
    categories=Category.objects.all()
    context = {
        'object_list':items,
        'categories':categories
    }
    return render(request,"cart/products.html",context)








class OrderSummary(LoginRequiredMixin,View):
    login_url="/login"
    def get(self,*args,**kwargs):
        try:
            order = Order.objects.get(user=self.request.user,ordered=False)
            context={
                'object': order
            }
            return render(self.request,"cart/order-summary.html",context)

        except ObjectDoesNotExist:
            messages.info(self.request,'You dont have any active order')
            return redirect('/')

        return render(self.request,"cart/order-summary.html")

# Adding Payment Gateway
import razorpay
razorpay_client = razorpay.Client(auth=(settings.razorpay_id, settings.razorpay_account_id))

@csrf_exempt
def handlerequest(request):
            messages.success(request,'Your order is placed Succesfully')
            return redirect('/')   
       

class Checkout(LoginRequiredMixin,View):
    login_url="/login"
    def get(self,*args,**kwargs):
        order =get_object_or_404(Order,user=self.request.user,ordered=False)
        form=AddressForm()
        context={
           'object': order,
           'form':form
        } 
        return render(self.request,"cart/checkout.html",context)


    def post(self,*args,**kwargs):
        form=AddressForm(self.request.POST or None)
        if form.is_valid():
            billingname=form.cleaned_data['billingname']
            address_1=form.cleaned_data['address_1']
            address_2=form.cleaned_data['address_2']
            city=form.cleaned_data['city']
            district=form.cleaned_data['district']
            zip_code=form.cleaned_data['zip_code']
            phone_number=form.cleaned_data['phone_number']
            order=get_object_or_404(Order,user=self.request.user,ordered=False)
            billing_address=BillingAddress.objects.create(user=self.request.user,billingname=billingname,address_1=address_1,address_2=address_2,city=city,district=district,zip_code=zip_code,phonenumber=phone_number)
            
            order.ordered=True
            order.billingaddress=billing_address
            order.total_price=order.get_total()
            for order_item in order.items.all():
                order_item.ordered=True
                order_item.save()

            total_order=TotalOrder.objects.create()
            total_order.totalorder.add(order)
            order.save()
                  #payment
        callback_url = 'http://127.0.0.1:8000/handlerequest/'
        print(callback_url)
        notes = {'order-type': "basic order from the website", 'key':'value'}
        razorpay_order = razorpay_client.order.create(dict(amount=order.total_price*100, currency='INR', notes = notes, receipt=f"{order.id}", payment_capture='0'))
        print(razorpay_order['id'])
        order.razorpay_order_id = razorpay_order['id']
        order.save()

        return render(self.request, 'cart/paymentsummaryrazorpay.html', {'order':order, 'order_id': razorpay_order['id'], 'orderId':order.id, 'total_price':order.total_price, 'razorpay_merchant_id':settings.razorpay_id, 'callback_url':callback_url})

        ##
            # mess=f"New order from {self.request.user.first_name} Order Id is {total_order.id} Total price:{order.total_price}  Please Check ASAP"
            # send_mail('New Order',mess,'singamhari34@gmail.com',['raohari12@gmail.com'],fail_silently=False)
            # mess1=f"Your Order has been placed succesfully"
            # send_mail('Greetings!',mess1,'raohari12gmail.com',[self.request.user.email],fail_silently=False)
            # messages.success(self.request,'your order is placed succesfully')
          

            
             

class OrderedView(LoginRequiredMixin,ListView):
    login_url="/login"
    template_name="cart/ordered.html"
    def get_queryset(self):
        return Order.objects.filter(user=self.request.user)
    


     
            
class ItemDetailView(DetailView):
    model = Items
    template_name="cart/product-detail.html"

 
class TotalOrderView(LoginRequiredMixin,ListView):
    login_url="/admin"
    template_name="cart/totalorder.html"  
    def get_queryset(self):
        user=self.request.user
        if(user.is_superuser):
            return TotalOrder.objects.all().order_by('-id')
        else:
            return 


    def post(self,*args,**kwargs):
        search=self.request.POST['search']
        if search=='':
            totalorder=TotalOrder.objects.all()
        
        else:    
            totalorder=TotalOrder.objects.filter(id=search) 
        context={
            'object_list':totalorder
        }
        return render(self.request,"cart/totalorder.html",context)
        
    
     


def signup(request):
    if request.method=='POST':
        get_otp=request.POST.get('otp')
        if get_otp:
            get_usr=request.POST['user']
            usr=User.objects.get(username=get_usr)
            if int(get_otp)==UserOtp.objects.filter(user=usr).last().otp:
                usr.is_active=True
                usr.save()
                return redirect('/login')
            else:
                messages.warning(request,"OTP is invalid")
                return render(request,'cart/signup.html',{'otp':True,'user':usr})

        else:
        
            first_name=request.POST['first_name']
            last_name=request.POST['last_name']
            password1=request.POST['password1']
            password2=request.POST['password2']
            email=request.POST['email']
            
            if password1==password2:    
                if User.objects.filter(email=email).exists(): 
                    messages.info(request,'Email Taken')
                    return redirect('/signup')


                    
                else:
                    user=User.objects.create_user(username=email,first_name=first_name,last_name=last_name,password=password1,email=email)
                    user.save()
                    otp=random.randint(100000,999999)
                    userotp=UserOtp.objects.create(user=user,otp=otp)

                    mess=f"{user.first_name} Your otp is {otp}"
                    send_mail('Welcome',mess,'ss',[email],fail_silently=False)
                    return render(request,'cart/signup.html',{'otp':True,'user':user})


            else:
                messages.info(request,'password mismatch')
                return render(request,'cart/signup.html')


    else:
        return render(request,'cart/signup.html')


def login(request):
    if request.method=='POST':
        username=request.POST['username']
        password=request.POST['password']

        user=auth.authenticate(username=username,password=password)
        if user is not None:
            auth.login(request,user)
            return redirect('/')

        else:
            messages.info(request,'Invalid Credentials')
            return redirect('/login')    

    else:
        
        return render(request,'cart/login.html')


def logout(request):
    auth.logout(request)      
    return redirect('/')

@login_required(login_url='/login')
def add_to_cart(request,slug):
    item=get_object_or_404(Items,slug=slug)
    order_item, created = OrderItem.objects.get_or_create(
        item=item,
        user=request.user,
        ordered=False
    )
    order_qs=Order.objects.filter(user=request.user,ordered=False)
    if order_qs.exists():
        order=order_qs[0]
        #check if the item is already in order
        if order.items.filter(item__slug=item.slug).exists():
            order_item.quantity += 1
            order_item.save()
            messages.info(request,'This Item is updated')
            return redirect("cart:order-summary")

        else:
            order.items.add(order_item)
            messages.info(request,'This item is added to cart')
            return redirect("cart:order-summary")

    else:
        ordered_date=timezone.now()
        user=Order.objects.create(user=request.user,ordered_date=ordered_date)
        user.items.add(order_item)
        messages.info(request,'This item is added to cart')
        return redirect("cart:order-summary")


@login_required(login_url='/login')
def remove_from_cart(request, slug):
    item = get_object_or_404(Items, slug=slug)
    order_qs = Order.objects.filter(user=request.user,ordered=False)
    if order_qs.exists():
        order = order_qs[0]
        if order.items.filter(item__slug=item.slug).exists():
            order_item = OrderItem.objects.filter(
                item=item,
                user=request.user,
                ordered=False
            )[0]
            order.items.remove(order_item)
            order_item.delete()
            messages.info(request,'This item was removed')
            return redirect("cart:order-summary")
        else:
            messages.info(request,'This item was not in your cart')
            return redirect("cart:order-summary")

    else:
        #duser dont have order
        messages.info(request,'user dont have order')
        return redirect("cart:product",slug=slug)       


@login_required(login_url='/login')
def remove_single_item_from_cart(request, slug):
    item = get_object_or_404(Items, slug=slug)
    order_qs = Order.objects.filter(user=request.user,ordered=False)
    if order_qs.exists():
        order = order_qs[0]
        if order.items.filter(item__slug=item.slug).exists():
            order_item = OrderItem.objects.filter(
                item=item,
                user=request.user,
                ordered=False
            )[0]
            order_item.quantity -= 1
            order_item.save()
            if order_item.quantity==0:
                order.items.remove(order_item)
                order_item.delete()
                return redirect("/")
        
            messages.info(request,'This item was updated')
            return redirect("cart:order-summary")
        else:
            messages.info(request,'This item was not in your cart')
            return redirect("cart:order-summary")

    else:
        #user dont have order
        messages.info(request,'user dont have order')
        return redirect("cart:product")        



def payment(request):
    if request.method == 'POST':
        order = Order.objects.get(user=request.user,ordered=False)
        order.ordered=True
        order.total_price=order.get_total()
        order.save()
        for order_item in order.items.all():
            order_item.ordered=True
            order_item.save()

        total_order=TotalOrder.objects.create()
        total_order.totalorder.add(order)
        paymentoption=request.POST['payment']
        bankingname=request.POST['bankingname']
        order.paymentoption=paymentoption
        order.bankingname=bankingname
        order.save()
  
        return render(request, 'cart/paymentsummaryrazorpay.html', {'order':order, 'order_id': razorpay_order['id'], 'orderId':order.order_id, 'total_price':order.total_price, 'razorpay_merchant_id':settings.razorpay_id, 'callback_url':callback_url})
    else:
        order = Order.objects.get(user=request.user,ordered=False)
        return render(request,'cart/payment.html',{'order':order})   


def export_csv(request):
    response=HttpResponse(content_type='text/csv')
    response['Content-Disposition']='attachment; filename=Expense'+ '.csv'
        
        
    writer=csv.writer(response)
    writer.writerow(['Orders','Order Id','User','Items','Price','Odered On','Billing Name','Phone Number','District','City','pincode','Address 1','Address 2','Delivered'])

    totalorder=TotalOrder.objects.all()
    for x in totalorder:
        for y in x.totalorder.all():
            
            writer.writerow(['',y.id,y.user.username,'',y.get_total(),y.ordered_date,y.billingaddress.billingname,y.billingaddress.phonenumber,y.billingaddress.district,y.billingaddress.city,y.billingaddress.zip_code,y.billingaddress.address_1,y.billingaddress.address_2,y.delivered
                ])
            for z in y.items.all():
                writer.writerow(['','','',z.item.title])
                


    return response


def update_order(request,slug):
    order=Order.objects.get(id=slug)
    if order.delivered:
        order.delivered=False
        order.save()
    else:
        order.delivered=True
        order.save()
    return redirect("cart:totalorder")


def delete_order(request,slug):
    order=TotalOrder.objects.get(id=slug)
    for x in order.totalorder.all():
        print(x)
        for y in x.items.all():
            y.delete()
        x.billingaddress.delete()    
        x.delete()
    order.delete()    

    return redirect("cart:totalorder")

def pdf_order(request,slug):   
    template_path='cart/orderpdf.html'
    order=get_object_or_404(Order,id=slug)
    torder=get_object_or_404(TotalOrder,totalorder=order)
    context={
        'order':order,
        'totalorder':torder
    }
    #create django response object and specify content_type as pdf
    response=HttpResponse(content_type='application/pdf')
    name=f"{order.user.username}"
    response['Content-Disposition']='attachment; filename="report.pdf"'
    #find the template and render it
    template=get_template(template_path)
    html = template.render(context)

    #create pdf
    pisa_status=pisa.CreatePDF(html,dest=response)
    if pisa_status.err:
        return HttpResponse('we had some errors <pre>'+html+'<pre>')
    return response    
