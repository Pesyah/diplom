from django.db import models
from optics.models import Optics

def validate_phone_number(value):
    return

    
class Optics_order_Manager(models.Manager):
    def create_order(self, optic, phone, email):
        order = self.create(optic=optic, phone=phone, email=email, current_price=optic.price)
        
        return order
        
class Optics_order(models.Model):
    
    optic = models.ForeignKey(Optics, models.SET_NULL, null=True)
    phone = models.CharField(max_length=15, validators=[validate_phone_number])
    email = models.EmailField(max_length=254)
    current_price = models.IntegerField()
    is_processed = models.BooleanField(default=False)
    is_completed = models.BooleanField(default=False)
    
    objects = Optics_order_Manager()

    def __str__(self) -> str:
        return self.phone
