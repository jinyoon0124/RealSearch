from django.db import models

# Create your models here.

class Reit_Indicator(models.Model):
    identifier = models.CharField(max_length=4)
    long_name = models.CharField(max_length=50)

    def __str__(self):
        return self.identifier + ' ' + self.long_name

class Industry_Info(models.Model):
    ind_name=models.CharField(max_length=50)
    price_to_equity=models.CharField(max_length=50)
    net_profit_margin=models.CharField(max_length=50)
    return_on_equity=models.CharField(max_length=50)
    dividend_yield=models.CharField(max_length=50)
    debt_to_equity=models.CharField(max_length=50)




