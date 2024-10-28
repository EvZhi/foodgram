from typing import Any
from django.contrib import admin
from django.forms.models import ModelForm
from django.http import HttpRequest

from .models import Subscription

admin.site.register(Subscription)


# class SubscriptionForm(ModelForm):
#     class Meta:
#         model = Subscription
#         fields = ('user', 'subscription')

# @admin.register(Subscription)
# class SubscriptionAdmin(admin.ModelAdmin):
#     form = SubscriptionForm
#     list_display = ('user', 'subscription')
#     fieldsets = [
#         (None, {'fields': ('user', 'subscription')} ),
#     ]

#     # readonly_fields = ('user',)

#     def get_form(self, request, obj, change, **kwargs):
#         form = super().get_form(request, obj, change, **kwargs)
#         form.user = request.user
#         return form
