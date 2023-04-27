from django.contrib import admin
from .models import Category, Genre, Title, Review, Comment, User

admin.site.register(Category)
admin.site.register(Genre)
admin.site.register(Title)
admin.site.register(Review)
admin.site.register(Comment)

@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    """User admin class."""
    list_display = ('pk', 'username', 'email', 'is_superuser',
                    'is_staff', 'role')
    search_fields = ('username',)
    list_filter = ('is_staff', 'role')
    list_editable = ('is_superuser', 'is_staff', 'role', 'email')
    empty_value_display = '-пусто-'
