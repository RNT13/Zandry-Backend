from django.contrib import admin

from .models import SubscriptionPlan
from .models import SubscriptionUsage

admin.site.register(SubscriptionPlan)
admin.site.register(SubscriptionUsage)
