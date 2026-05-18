from django.contrib import admin

from .models import SubscriptionPlan, SubscriptionUsage

admin.site.register(SubscriptionPlan)
admin.site.register(SubscriptionUsage)
