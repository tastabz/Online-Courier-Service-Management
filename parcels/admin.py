from decouple import config
from django.contrib import admin
from django.core.mail import send_mail

from .models import Parcel, Issue, Address, Receiver


# Register your models here.

"""Admin controller for parcels."""

@admin.register(Address)
class AddressAdmin(admin.ModelAdmin):
    """
    This class controls admin access to address data.

    :ivar list_display: List of fields name to display in listview.
    :vartype list_display: list
    """

    list_display = ['country', 'city', 'street', 'zip', ]

    def save_model(self, request, obj, form, change):
        """
        Function will be called if admin save any address.

        :param request: Request from admin.
        :param obj: Requested object to save.
        :param form: Forms with data.
        :param change: If there is any change.
        :return: None
        """
        super().save_model(request, obj, form, change)


@admin.register(Receiver)
class ReceiverAdmin(admin.ModelAdmin):
    """
    This class controls admin access to receivers data.

    :ivar list_display: List of fields name to display in listview.
    :vartype list_display: list
    """

    list_display = ['name', 'email', 'phone', ]

    def save_model(self, request, obj, form, change):
        """
        Function will be called if admin save any receiver.

        :param request: Request from admin.
        :param obj: Requested object to save.
        :param form: Forms with data.
        :param change: If there is any change.
        :return: None
        """
        super().save_model(request, obj, form, change)


class IssueInline(admin.TabularInline):
    """
    Issue inline class to show inline issues in parcels.

    :ivar model: Base model of IssuInline.
    :vartype model: Issue
    """

    model = Issue


@admin.register(Issue)
class IssueAdmin(admin.ModelAdmin):
    """
    This class controls admin access to issue data.

    :ivar list_display: List of fields name to display in listview.
    :vartype list_display: list

    :ivar readonly_fields: List of fields name that admins can only read.
    :vartype readonly_fields: list
    """

    list_display = ['category', 'status', 'parcel', ]
    readonly_fields = ['parcel', 'message', ]

    def save_model(self, request, obj, form, change):
        """
        Function will be called if admin save any issue.

        :param request: Request from admin.
        :param obj: Requested object to save.
        :param form: Forms with data.
        :param change: If there is any change.
        :return: None
        """

        super().save_model(request, obj, form, change)


@admin.register(Parcel)
class ParcelAdmin(admin.ModelAdmin):
    """
    This class controls admin access to parcels data.

    :ivar list_display: List of fields name to display in listview.
    :vartype list_display: list

    :ivar readonly_fields: List of fields name that admins can only read.
    :vartype readonly_fields: list
    """

    list_display = ['id', 'status']
    readonly_fields = ['pickup_address', 'receiver', 'booked_by', ]
    inlines = [
        IssueInline,
    ]

    def save_model(self, request, obj, form, change):
        """
        Function will be called if admin save any parcel.

        :param request: Request from admin.
        :param obj: Requested object to save.
        :param form: Forms with data.
        :param change: If there is any change.
        :return: None
        """
        super().save_model(request, obj, form, change)
        if change:
            message = f"You are receiving this email because you have a parcel at {request.META['HTTP_HOST']}."

            if 'status' in form.changed_data:
                message += f"\n\nYour parcel has been {obj.status}."

            if 'delivery_agent' in form.changed_data:
                message += f"\n\nDelivery agent {obj.delivery_agent.get_full_name()} has been assigned to your parcel."

            message += f"Please visit our website to know more." + \
                       f"\n\nYour parcel tracking ID, in case you’ve forgotten: {obj.id}" + \
                       f"\n\nThanks for using our service!" + \
                       f"\n\nThe {request.META['HTTP_HOST']} team"

            send_mail(
                subject='Parcel Update',
                message=message,
                from_email=config('EMAIL'),
                recipient_list=[obj.booked_by.email],
            )
