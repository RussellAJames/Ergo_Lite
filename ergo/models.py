from django.db import models
from django.core.validators import RegexValidator
import base58

from ergo.validators import validate_address
# Create your models here.


class wallet(models.Model):
    print('hello??')
    address = models.CharField(
        max_length=300, 
        
        validators=[validate_address
        ]
        
        
        
        
        )



    class Meta:
        ordering = ['-address']

