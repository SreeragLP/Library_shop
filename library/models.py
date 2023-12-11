from django.db import models

# Create your models here.
class Category(models.Model):
    cname=models.CharField(max_length=200)
    description=models.TextField()
    image=models.ImageField(upload_to='shop/category',null=True,blank=True)

    def __str__(self):
        return self.cname


class Books(models.Model):
    bname = models.CharField(max_length=200)
    auther=models.CharField(max_length=100)
    description = models.TextField()
    image = models.ImageField(upload_to='library/books', null=True, blank=True)
    price=models.DecimalField(max_digits=10,decimal_places=2)
    category=models.ForeignKey(Category,on_delete=models.CASCADE)
    stock=models.IntegerField()
    available=models.BooleanField(default=True)
    created=models.DateTimeField(auto_now_add=True)
    updated=models.DateTimeField(auto_now=True)
    pdf = models.FileField(upload_to='library/pdf', null=True, blank=True)
    publisher = models.CharField(max_length=100, null=True, blank=True)
    language = models.CharField(max_length=50, null=True, blank=True)
    num_pages = models.IntegerField(null=True, blank=True)
    book_format = models.CharField(max_length=50, null=True, blank=True)

    def __str__(self):
        return self.bname
