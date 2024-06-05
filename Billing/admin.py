from django.contrib import admin
from Billing.models import Billing, Promotion, Coupon

# Register your models here.

admin.site.register(Billing)
admin.site.register(Promotion)
admin.site.register(Coupon)