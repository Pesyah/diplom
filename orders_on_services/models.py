from django.db import models
from services.models import Services


class Services_order_Manager(models.Manager):
    def create_order(self, services, phone, email, time):
        order = self.create(services=services, phone=phone, email=email, current_price=services.price, time=time)

        return order
        
class Services_order(models.Model):
    
    services = models.ForeignKey(Services, models.SET_NULL, null=True)
    phone = models.CharField(max_length=15)
    email = models.EmailField(max_length=254)
    current_price = models.IntegerField()
    time = models.DateTimeField()
    is_processed = models.BooleanField(default=False)
    is_completed = models.BooleanField(default=False)
    
    objects = Services_order_Manager()

    def __str__(self) -> str:
        return self.phone
