from django.db import models
from library.models import Books
from django.contrib.auth.models import User
from decimal import Decimal

# Create your models here.

class Cart(models.Model):
    book=models.ForeignKey(Books,on_delete=models.CASCADE)
    user = models.ForeignKey(User,on_delete=models.CASCADE)
    quantity=models.IntegerField()
    date_added=models.DateField(auto_now_add=True)

    def subtotal(self):
        return self.quantity * self.book.price




class Order(models.Model):
    book=models.ForeignKey(Books,on_delete=models.CASCADE)
    user=models.ForeignKey(User,on_delete=models.CASCADE)
    noofitems=models.IntegerField()
    address=models.TextField(max_length=200)
    phone=models.CharField(max_length=200)
    order_status=models.CharField(max_length=30, default="pending")
    delivery_status=models.CharField(max_length=30, default="pending")
    date_added=models.DateTimeField(auto_now=True)
    payment_method = models.CharField(max_length=50, default="credit card")

    def __str__(self):
        return str(self.user)

    def subtotal(self):
        return self.noofitems * self.book.price


    def grand_total(self):
        total = self.subtotal()
        gst_rate = Decimal('0.12')
        shipping_charge = 0

        if total < 700:
            shipping_charge += 50

        gst = round(total * gst_rate, 2)
        grand_total = total + gst + shipping_charge

        return grand_total


class Account(models.Model):
    accnumber=models.IntegerField()
    acctype=models.CharField(max_length=200)
    balance = models.DecimalField(max_digits=10, decimal_places=2)



    def __str__(self):
        return str(self.accnumber)


