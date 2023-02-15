from django.contrib import admin

from parcels.models import Parcel
from .models import Customer, DeliveryAgent


# Register your models here.

"""Admin controller for users."""


class CustomerParcelInline(admin.TabularInline):
    """
    Parcel inline class to show inline parcels of customers.

    :ivar model: Base model of CustomerParcelInline.
    :vartype model: Parcel

    :ivar fk_name: Foreign key field.
    :vartype fk_name: str
    """

    model = Parcel
    fk_name = 'booked_by'


class DeliveryAgentParcelInline(admin.TabularInline):
    """
    Parcel inline class to show inline parcels of delivery agents.

    :ivar model: Base model of DeliveryAgentParcelInline.
    :vartype model: Parcel

    :ivar fk_name: Foreign key field.
    :vartype fk_name: str
    """

    model = Parcel
    fk_name = 'delivery_agent'


@admin.register(Customer)
class CustomerAdmin(admin.ModelAdmin):
    """
    This class controls admin access to customers data.

    :ivar list_display: List of fields name to display in listview.
    :vartype list_display: list

    :ivar exclude: List of fields name to exclude from admin view.
    :vartype exclude: list

    :ivar readonly_fields: List of fields name that admins can only read.
    :vartype readonly_fields: list

    :ivar inlines: List of inline views.
    :vartype inlines: list
    """

    list_display = ['email']
    exclude = ['password', ]
    readonly_fields = ['last_login', 'date_joined', ]
    inlines = [
        CustomerParcelInline
    ]

    def save_model(self, request, obj, form, change):
        """
        Function will be called if admin save any customer.

        :param request: Request from admin.
        :param obj: Requested object to save.
        :param form: Forms with data.
        :param change: If there is any change.
        :return: None
        """

        super().save_model(request, obj, form, change)


@admin.register(DeliveryAgent)
class DeliveryAgentAdmin(admin.ModelAdmin):
    """
    This class controls admin access to delivery-agents data.

    :ivar list_display: List of fields name to display in listview.
    :vartype list_display: list

    :ivar exclude: List of fields name to exclude from admin view.
    :vartype exclude: list

    :ivar readonly_fields: List of fields name that admins can only read.
    :vartype readonly_fields: list

    :ivar inlines: List of inline views.
    :vartype inline: list
    """

    list_display = ['id']
    exclude = ['password', ]
    readonly_fields = ['last_login', 'date_joined', ]
    inlines = [
        DeliveryAgentParcelInline
    ]

    def save_model(self, request, obj, form, change):
        """
        Function will be called if admin save any delivery-agent.

        :param request: Request from admin.
        :param obj: Requested object to save.
        :param form: Forms with data.
        :param change: If there is any change.
        :return: None
        """

        super().save_model(request, obj, form, change)
