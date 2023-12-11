from django.shortcuts import render,redirect
from cart.models import Cart
from library.models import Books
from decimal import Decimal
from cart.models import Account,Order
from django.contrib.auth.decorators import login_required


def add_to_cart(request, p):
    if request.user.is_authenticated:  #its for login required purpose
        book = Books.objects.get(bname=p)
        user = request.user
        try:                                                  #if one item alredy in cart we dont want same item repete,
            cart = Cart.objects.get(user=user, book=book)
            if cart.quantity < cart.book.stock:                #we can only add items if we have stock in hand.
                cart.quantity += 1                             #we only want to increase quantity.
            cart.save()
        except Cart.DoesNotExist:
            cart = Cart.objects.create(book=book, user=user, quantity=1)
            cart.save()
        return redirect('cart:cart_view')
    else:
        return redirect('library:login')                          #if user ain't login it shows login page



@login_required
def cart_view(request):
    if request.user.is_authenticated: #its for login required purpose

        user = request.user
        cart = Cart.objects.filter(user=user)


        total = 0
        gst_rate = Decimal('0.12')        #12% igst tax (12/100)
        shipping_charge = 0

        for i in cart:
            total += i.quantity * i.book.price

        if total < 700:
            shipping_charge+= shipping_charge+50  # adding shipping charge 50 if total less than 700

        gst = round (total * gst_rate,2)

        grand_total = total + gst + shipping_charge

        return render(request, 'cart/cartview.html', {
            'cart': cart,
            'total': total,
            'shipping_charge': shipping_charge,
            'gst': gst,
            'grand_total': grand_total,
        })
    else:
        return redirect('library:login')



@login_required
def cart_remove(request,p):
    book=Books.objects.get(bname=p)
    user=request.user
    try:
        cart=Cart.objects.get(user=user,book=book)

        if(cart.quantity>1):
            cart.quantity-=1
            cart.save()

        else:
            cart.delete()

    except:
        pass
    return redirect('cart:cart_view')


@login_required
def full_remove(request,p):
    book = Books.objects.get(bname=p)
    user = request.user
    try:
        cart = Cart.objects.get(user=user, book=book)
        cart.delete()
    except:
        pass
    return redirect('cart:cart_view')




@login_required
def order_form(request):
    if request.method == "POST":
        a = request.POST['a']  # Address
        p = request.POST['p']  # Phone
        payment_method = request.POST.get('payment_method')


        user = request.user
        cart = Cart.objects.filter(user=user) #flitering the user's items


        total = 0
        gst_rate = Decimal('0.12')  # 12% igst tax (12/100)
        shipping_charge = 0

        for i in cart:
            total += i.quantity * i.book.price

        if total < 700:
            shipping_charge += shipping_charge + 50  # adding shipping charge 50 if total less than 700

        gst = round(total * gst_rate, 2)

        grand_total = total + gst + shipping_charge

        if payment_method == 'select':
            msg='Please select a valid payment method'


        if payment_method == 'cod':  #if user choose cash on payment
            for i in cart:
                order = Order.objects.create(
                    user=user, book=i.book, phone=p, address=a,
                    noofitems=i.quantity, order_status="pending",   #becoz we are paying in the time of delivery
                    payment_method="cod")
                order.save()
                i.book.stock -= i.quantity   #its for deducting from stock
                i.book.save()
            cart.delete()                        #because we dont need the cart after ordering
            msg = 'Order placed successfully with Cash on Delivery (COD). You will pay upon delivery.'



        elif payment_method == 'online':   #if user selects online payment
            n = request.POST.get('n')  # Account Number

            #(if customer type incorrect account number , there is try and exception)
            try:
                acct = Account.objects.get(accnumber=n)

            except Account.DoesNotExist:                         #if cutomer type wrong account number
                msg = "Account number doesn't exist."
                return render(request, 'cart/orderconfirm.html', {'msg': msg})

            if acct.balance >= grand_total:    #our order total musn't exceeds acc balace
                acct.balance = acct.balance - grand_total  #deducting amount total from accot blanc
                acct.save()

                for i in cart:
                    order = Order.objects.create(
                        user=user, book=i.book, phone=p, address=a,
                        noofitems=i.quantity, order_status="paid",    #in the case of online payment, we already paid the amout
                        payment_method="online")

                    order.save()
                    i.book.stock -= i.quantity     #deducting ordered books quantity from our stock
                    i.book.save()
                cart.delete()
                msg = 'Order placed successfully with online payment.'


            else:
                msg = "Insufficient amount. You can't place the order."

        return render(request, 'cart/orderconfirm.html', {'msg': msg})

    return render(request, 'cart/orderform.html')






@login_required
def orderview(request):
    user = request.user
    o = Order.objects.filter(user=user)
    return render(request,'cart/orderview.html',{'o': o,'u':user.username})


