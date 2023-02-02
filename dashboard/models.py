from tabnanny import verbose
from django.db import models
from django.contrib.auth.models import User

# Create your models here.
CATEGORY = (

    ('Stationary', 'Stationary'),
    ('Electronics', 'Electronics'),
    ('Food', 'Food')
)


class Product(models.Model):

    name = models.CharField(max_length=100, null=True)
    category = models.CharField(max_length=20, choices=CATEGORY, null=True)
    quantity = models.PositiveIntegerField(null=True)

    def __str__(self) -> str:
        
        return f'{self.name}' 



class Order(models.Model):

    product = models.ForeignKey(Product, on_delete=models.CASCADE, null=True)
    staff = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    quantity = models.PositiveIntegerField(null=True)
    out = models.BooleanField()
    date = models.DateTimeField(auto_now_add=True)



    def __str__(self) -> str:
        return f'{self.product} ordered by {self.staff}'


class OrderMessage(models.Model):

    name = models.CharField(max_length=200, null=True)
    invoice = models.TextField()
    date = models.DateTimeField(auto_now_add=True)

    def __str__(self) -> str:
        return f'{self.name} order out of stock'









