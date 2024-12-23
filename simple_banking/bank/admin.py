from django.contrib import admin
from .models import Customer, Account, Transaction, Loan, User

admin.site.register(Customer)
admin.site.register(Account)
admin.site.register(Transaction)
admin.site.register(Loan)
admin.site.register(User)


'''class CustomerAdmin(admin.ModelAdmin):
    list_display = ('first_name', 'last_name', 'email', 'phone', 'created_at')
    search_fields = ('first_name', 'last_name', 'email')

admin.site.register(Customer, CustomerAdmin)'''
