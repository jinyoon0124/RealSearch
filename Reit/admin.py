from django.contrib import admin

# Register your models here.
from Reit.models import Reit_Indicator, Industry_Info

class nameAdmin(admin.ModelAdmin):
    fields = ['long_name', 'identifier']
    list_display = ('long_name', 'identifier')
    list_filter = ['long_name']
    search_fields = ['identifier']

#class industryAdmin(admin.ModelAdmin):
#    fields = ['ind_name', 'price_to_equity', 'net_profit_margin', 'return_on_equity', 'dividend_yield', 'debt_to_equity']
#    list_display = ('ind_name', 'price_to_equity', 'net_profit_margin', 'return_on_equity', 'dividend_yield', 'debt_to_equity')
#    list_filter = ['ind_name']
#    search_fields = ['ind_name']


admin.site.register(Reit_Indicator,nameAdmin)
#admin.site.register(Industry_Info, nameAdmin)