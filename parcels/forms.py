from django import forms

from parcels.models import Parcel, Address, Receiver

"""List of parcels forms."""


class ParcelTrackForm(forms.Form):
    """Parcel track form to get tracking id from users."""

    parcel_id = forms.IntegerField()


class CostCalculatorForm(forms.Form):
    """Cost calculator form."""

    AREA = [
        ('inside', 'Inside Dhaka'),
        ('outside', 'Outside Dhaka'),
    ]

    weight = forms.IntegerField()
    area = forms.ChoiceField(choices=AREA)


class AddressForm(forms.ModelForm):
    """Model address form. This form will be used to take address information from the users."""

    class Meta:
        model = Address
        fields = '__all__'


class ReceiverForm(forms.ModelForm):
    """Model receiver form. This form will be used to take receiver information from the users."""

    class Meta:
        model = Receiver
        exclude = ['address']


class ParcelForm(forms.ModelForm):
    """Model parcel form. This form will be used to take parcel information from the users."""

    class Meta:
        model = Parcel
        fields = ['type', ]
