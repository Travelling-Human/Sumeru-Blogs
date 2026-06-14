from django.contrib import admin
from django.contrib import admin
from .models import Post, Comment, Category
#from accounts.models import CustomUser

#admin.site.register(CustomUser)
admin.site.register(Post)
admin.site.register(Comment)
admin.site.register(Category)