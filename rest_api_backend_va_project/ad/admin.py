from django.contrib import admin
from .models import Ad


class AdAdmin(admin.ModelAdmin):
    list_display = (
        'title', 'author', 'city', 'number_of_person', 'number_of_girls',
        'number_of_boys', 'party_date', 'is_published','create_ad'
    )
    list_filter = ('city', 'party_date')

    readonly_fields = ('title', 'author', 'city', 'number_of_person', 'number_of_girls', 'number_of_boys', 'party_date', 'geolocation', 'create_ad')


admin.site.register(Ad, AdAdmin)
