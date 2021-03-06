from django.contrib import admin

# Register your models here.
from .models import Account
from django.contrib.auth.admin import UserAdmin





class AccountAdmin(UserAdmin):

	list_display = ('email','username','date_joined', 'last_login', 'is_admin','is_staff')

	search_fields = ('email','username',)

	readonly_fields=('date_joined', 'last_login')  #the fields that can't be change

	filter_horizontal = ()
	list_filter = ()
	fieldsets = ()


# Register your models here.


admin.site.register(Account, AccountAdmin)