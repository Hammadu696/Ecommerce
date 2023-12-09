from django.shortcuts import get_object_or_404, redirect, render
from .models import Item, Order,OrderItem
from django.utils import timezone
from django.views.generic import ListView, DetailView
# Create your views here.
# def item_list(request):
#     context = {
#         'items':Item.objects.all(),
        
#     }
#     return render(request,"home-page.html",context)


class  HomeView (ListView):
    model = Item
    template_name = "home.html"


class  ItemDetailView (DetailView):
    model = Item
    template_name = "product.html"


def add_to_cart(request, slug):
    item = get_object_or_404(Item,slug=slug)
    order_item , created =OrderItem.objects.get_or_create(item = item, user = request.user,ordered =False)
    order_qs= Order.objects.filter(user= request.user, ordered =False)
    print("enter in function")
    if order_qs.exists() :
        order =order_qs[0]
        if order.items.filter(item__slug=item.slug).exists():
            order_item.quantity +=1
            order_item.save()
        else:
            order.items.add(order_item)
    else:
        ordered_date = timezone.now()
        print("enter else")
        order = Order.objects.create(user =request.user,ordered_date=ordered_date)
        order.items.add(order_item)
    return redirect("core:product",slug =slug) 


def remove_from_cart(request,slug):
    item = get_object_or_404(Item,slug=slug)
    order_qs= Order.objects.filter(user= request.user, ordered =False)
   
    if order_qs.exists() :
        order =order_qs[0]
        #check if the item is in the order
        if order.items.filter(item__slug=item.slug).exists():
            order_item = OrderItem.objects.filter(item=item,user= request.user,ordered =False)[0]
            order.items.remove(order_item)
        else:
            # add msg syaing item does not in order 
            return redirect("core:product",slug =slug) 
    else:
        ordered_date = timezone.now()
        print("enter else")
        order = Order.objects.create(user =request.user,ordered_date=ordered_date)
        order.items.add(order_item)
    return redirect("core:product",slug =slug) 