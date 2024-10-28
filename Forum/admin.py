from django.contrib import admin
from .models import Channel, Post, Comment

admin.site.register(Channel)
admin.site.register(Post)
admin.site.register(Comment)