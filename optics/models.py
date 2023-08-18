from django.db import models

class Optics(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()
    price = models.IntegerField()
    picture = models.ImageField()

    def __str__(self) -> str:
        return self.name
    
    def getOptic(self):
        return { 'id': self.id,
                'name': self.name,
                'description': self.description,
                'price': self.price,
                'picture': self.picture}