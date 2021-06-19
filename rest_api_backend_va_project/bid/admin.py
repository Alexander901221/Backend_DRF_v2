from django.contrib import admin
from .models import Bid


class BidAdmin(admin.ModelAdmin):
    list_display = ("author", "ad", "number_of_person", 'number_of_girls', 'number_of_boys', 'create_ad')
    list_filter = ("ad__title", "create_ad")
    pass


admin.site.register(Bid, BidAdmin)
