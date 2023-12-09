from django.db import models
from django.conf import settings
from django.shortcuts import reverse

# Create your models here.
class Item(models.Model):
    title = models.CharField(max_length=100)
    price = models.FloatField()
    desc = models.TextField()
    slug = models.SlugField()
    
    def __str__(self):
        return self.title
    
    def get_absolute_url(self):
        return reverse("core:product", kwargs={"slug": self.slug})
    
    def get_add_to_cart(self):
        return reverse("core:product", kwargs={"slug": self.slug})
    


class OrderItem(models.Model):
    item =models.ForeignKey(Item, on_delete=models.CASCADE)
    quantity = models.IntegerField(default=1)


class Order(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL,on_delete=models.CASCADE)
    items= models.ManyToManyField(OrderItem)
    start_date= models.DateTimeField(auto_now_add=True)
    ordered_date=models.DateTimeField()
    Ordered =  models.BooleanField(default=False)

    def __str__(self):
        return self.user.username
