from django.contrib import admin
from django.utils.safestring import mark_safe

from .models import User, Subscription


class UserAdmin(admin.ModelAdmin):
    list_display = ("username", "first_name", "email", "get_image", "date_joined")
    list_filter = ("date_joined", "is_superuser")

    def get_image(self, obj):
        if obj.photo:
            print('obj.photo.url ==> ', obj.photo.url)
            return mark_safe(f'<img src={obj.photo.url} width="50" height="60"')
        else:
            return mark_safe(f'<img src="" alt="" width="50" height="60"')

    get_image.short_description = "Изображение"


admin.site.site_header = "Административная панель VA"
admin.site.index_title = "Модели"
admin.site.register(User, UserAdmin)


class SubscriptionAdmin(admin.ModelAdmin):
    pass


admin.site.register(Subscription, SubscriptionAdmin)
