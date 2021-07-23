from django.contrib import admin

from .models import Participant


class ParticipantAdmin(admin.ModelAdmin):
    list_display = ("user", "ad", "number_of_person", "number_of_girls", "number_of_boys", "create_ad")
    list_filter = ("ad__city", "create_ad")


admin.site.register(Participant, ParticipantAdmin)
