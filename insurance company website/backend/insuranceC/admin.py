from django.contrib import admin
from .models import Insurance, UserInsurance

class InsuranceAdmin(admin.ModelAdmin):
    list_display = ('package_name', 'price', 'coverage_limit', 'cover')
    search_fields = ('package_name',)
    list_filter = ('price', 'coverage_limit')

class UserInsuranceAdmin(admin.ModelAdmin):
    list_display = ('user', 'insurance', 'purchase_date', 'expiry_date', 'is_active')
    search_fields = ('user__username', 'insurance__package_name')
    list_filter = ('is_active',)
    readonly_fields = ('purchase_date',)

admin.site.register(Insurance, InsuranceAdmin)
admin.site.register(UserInsurance, UserInsuranceAdmin)
