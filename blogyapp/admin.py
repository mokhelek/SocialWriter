from django.contrib import admin
from .models import  Entry , Comments , Notification ,Like , Bookmark

# Register your models here.
admin.site.register(Entry)
admin.site.register(Comments)
admin.site.register(Notification)
admin.site.register(Like)
admin.site.register(Bookmark)
