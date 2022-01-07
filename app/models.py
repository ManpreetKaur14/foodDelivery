from django.db import models

# Create your models here.
    
class Menu(models.Model):
    dishId = models.IntegerField(unique=True)
    dishName = models.CharField(max_length=100)
    dishDescription = models.CharField(max_length=100, null=True)
    dishPrice = models.IntegerField()
    dishImage=models.ImageField(upload_to='food_images/')
    searchTag=models.CharField(max_length=250)
    isBanner=models.BooleanField(default=False)
    isPopular=models.BooleanField(default=False)
    def __str__(self):
        return self.dishName
    