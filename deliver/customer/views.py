from django.shortcuts import render
from django.views import View
from django.core.mail import send_mail
from .models import MenuItem, Category, OrderModel


class Index(View):
    def get(self, request, *args, **kwargs):
        return render(request, 'customer/index.html')
    
class About(View):
    def get(self, request, *args, **kwargs):
        return render(request, 'customer/about.html')

class Order(View):
    def get(self, request, *args, **kwargs):
        breakfast = MenuItem.objects.filter(category__name__contains='Breakfast')
        lunch = MenuItem.objects.filter(category__name__contains='Lunch')
        dessert = MenuItem.objects.filter(category__name__contains='Dessert')
        drinks = MenuItem.objects.filter(category__name__contains='Drinks')

        context = {
            'breakfast' : breakfast,
            'lunch' : lunch,
            'dessert' : dessert,
            'drinks' : drinks,
        }

        return render (request, 'customer/order.html', context)
    
    def post(self, request, *args, **kwargs):
        name = request.POST.get('name')
        email = request.POST.get('email')
        address = request.POST.get('address')

        order_items ={
            'items': []
        }
        items = request.POST.getlist('items[]')

        for item in items:
            if item.strip() and item.strip() .isdigit():
                menu_item = MenuItem.objects.get(pk=int(item))
                item_data = {
                    'id': menu_item.pk,
                    'name': menu_item.name,
                    'price' : menu_item.price
                }
                order_items['items'].append(item_data)
            else:
                print(f"Skipping Invalid Item: {repr(item)}")

        price = 0
        item_ids = []

        for item in order_items['items']:
            price += item['price']
            item_ids.append(item['id'])

        order = OrderModel.objects.create(
            price=price,
            name=name,
            email=email,
            address=address
        )
        order.items.add(*item_ids)

        # After everything, send confirmation email to user
        body = ('Thank you for your order! Your food is being prepared and will be delivered soon!\n'
                f'Your Total: {price}\n'
                'Thank you again for your order!')
        
        send_mail(
            'Thank You For Your Order!',
            body,
            'example@example.com',
            [email],
            fail_silently=False
        )

        context = {
            'items' : order_items['items'],
            'price' : price
        }
            
        return render (request, 'customer/order_confirmation.html', context)

                

    

