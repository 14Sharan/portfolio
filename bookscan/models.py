from django.db import models
import datetime 

from django.contrib.auth.models import User


COUNTRY_CHOICES = (
    ('','Select Country'),
    ('Bangladesh','Bangladesh'),
    ('China', 'China'),
    ('country','country'),
    ('India','India'),
    ('Japan','Japan'),
)

class Customer(models.Model):
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    phone = models.CharField(max_length=10)
    email = models.EmailField()
    password = models.CharField(max_length=100)

    class Meta:
        db_table = 'customer'


class Category(models.Model):
    name = models.CharField(max_length=50)
  
    @staticmethod
    def get_all_categories():
        return Category.objects.all()
  
    def __str__(self):
        return self.name

class Products(models.Model):
    name = models.CharField(max_length=60)
    price = models.IntegerField(default=0)
    category = models.ForeignKey(Category, on_delete=models.CASCADE, default=1)
    description = models.CharField(
        max_length=250, default='', blank=True, null=True)
    image = models.ImageField(upload_to='products/')

    class Meta:
        db_table = 'product'

    def __str__(self):
        return self.name


class Order(models.Model):
    product = models.ManyToManyField(Products)
    customer = models.ForeignKey(Customer,
                                 on_delete=models.CASCADE, null=True, blank=True)
    price = models.FloatField()
    address_line1 = models.CharField(max_length=50, null=True, blank=True)
    address_line2 = models.CharField(max_length=50, null=True, blank=True)
    phone_number = models.CharField(max_length=50, null=True, blank=True)
    town_city = models.CharField(max_length=50, null=True, blank=True)
    state = models.CharField(max_length=50, null=True, blank=True)
    first_name = models.CharField(max_length=20)
    last_name = models.CharField(max_length=20)
    company_name = models.CharField(max_length=200)
    zipcode = models.CharField(max_length=50, null=True, blank=True)
    date = models.DateField(default=datetime.datetime.today)
    status = models.BooleanField(default=False)
    country = models.CharField(max_length=10, choices=COUNTRY_CHOICES)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    notes = models.TextField()
    email = models.EmailField()
    
    class Meta:
        db_table = 'order'


class Author(models.Model):
    profile_image = models.ImageField(upload_to='authors/')
    first_name = models.CharField(max_length=20)
    last_name = models.CharField(max_length=20)
    dob = models.DateField()
    author_bio = models.TextField()
    product = models.ForeignKey(Products, on_delete=models.CASCADE, default=1, related_name='products')

    class Meta:
        db_table = 'author'

    def __str__(self):
        return f'{self.first_name} {self.last_name}'


class Cart(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    item = models.ForeignKey(Products, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)
    total_price = models.FloatField()

    class Meta:
        db_table = 'cart'

    # def __str__(self):
    #     return self.item.book_title


class ContactDetails(models.Model):
    email = models.EmailField(null=True,blank=True)
    name = models.CharField(max_length=200,null=True,blank=True)
    phone_number = models.CharField(max_length=15,null=True,blank=True)
    message = models.TextField(null=True,blank=True)

    class Meta:
        db_table = 'contacts'

    def __str__(self):
        return self.name


class Banner(models.Model):
    name = models.CharField(max_length=200)
    description = models.CharField(max_length=200)
    image = models.FileField(upload_to="banner",null=True,blank=True)
    