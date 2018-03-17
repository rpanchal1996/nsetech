from django.db import models

# Create your models here.
class stock(models.Model):
	Date = models.DateTimeField()
	quantity = models.IntegerField()
	price_per_unit = models.IntegerField()
	stock_name = models.CharField(max_length=100)