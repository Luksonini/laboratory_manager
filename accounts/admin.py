from django.contrib import admin
from .models.user import User  # zaimportuj model User

@admin.register(User)  # zarejestruj model User za pomocą dekoratora
class UserAdmin(admin.ModelAdmin):
    list_display = ('email', 'is_staff', 'is_active', 'date_joined', 'last_updated', 'is_verified')  # określ, które pola mają być wyświetlane w panelu administratora
    list_filter = ('is_staff', 'is_active', 'is_verified')  # określ filtry, które mają być dostępne
    search_fields = ('email',)  # określ pola, według których będzie można przeszukiwać