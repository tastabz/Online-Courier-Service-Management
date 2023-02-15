from django import forms
from django.contrib.auth.forms import UserCreationForm

from .models import Customer

"""List of forms of users."""


class CustomerCreationForm(UserCreationForm):
    """
    This form will be used to take information from the users to create customer account.

    :ivar first_name: First name of the customer.
    :vartype first_name: django.forms.CharField

    :ivar last_name: Last name of the customer.
    :vartype last_name: django.forms.CharField

    :ivar email: Email of the customer.
    :vartype email: django.forms.EmailField

    :ivar phone: Phone number of the customer.
    :vartype phone: django.forms.CharField
    """
    first_name = forms.CharField(max_length=30, required=False, help_text='Optional')
    last_name = forms.CharField(max_length=30, required=False, help_text='Optional')
    email = forms.EmailField(max_length=254, help_text='Required. Inform a valid email address.')
    phone = forms.CharField(max_length=200)

    class Meta:
        """
        Meta class of CustomerCreationForm.

        :ivar model: Model to use to create customer.
        :vartype model: django.db.models.Model

        :ivar fields: Name of the fields in the form.
        :vartype fields: list
        """
        model = Customer
        fields = ['username', 'first_name', 'last_name', 'email', 'phone', 'password1', 'password2', ]
