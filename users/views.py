from django.contrib.auth.mixins import UserPassesTestMixin
from django.contrib.auth.models import User
from django.shortcuts import render
from django.views import generic

from users.models import Customer
from .forms import CustomerCreationForm


# Create your views here.

"""List of users views."""


def home(request):
    """
    Function for requesting home page view.

    :param request: Type of request from user.
    :type request: request

    :return: Return render view with index.html.
    :rtype: django.shortcuts.render
    """
    return render(request, 'index.html')


# fixme: think about the access of the views
# todo: access modifier


class UserDetailView(UserPassesTestMixin, generic.DetailView):
    """
    This class handles all the detail view requests from user.

    :ivar model: Base model of UserDetailView.
    :vartype model: django.db.models.Model

    :ivar template_name: Name of the template to render UserDetailView.
    :vartype template_name: str
    """

    def test_func(self):
        """
        Function for checking access permission of requesting user to this view.

        :return: return true if user passes test
        :rtype: bool
        """
        return True

    model = User
    template_name = 'users/user_detail.html'


class CustomerDetailView(UserPassesTestMixin, generic.DetailView):
    """
    This class handles all the detail view requests from customer.

    :ivar model: Base model of CustomerDetailView.
    :vartype model: django.db.models.Model

    :ivar template_name: Name of the template to render CustomerDetailView.
    :vartype template_name: str
    """

    def test_func(self):
        """
        Function for checking access permission of requesting user to this view.

        :return: Return true if user passes test.
        :rtype: bool
        """
        return True

    model = Customer
    template_name = 'users/customer_detail.html'


class CustomerCreationView(generic.edit.CreateView):
    """
    This class is responsible to handle Customer creation requests.

    :ivar form_class: Form to pass when creating Customer.
    :vartype form_class: django.forms.Form

    :ivar template_name: Name of the template to render CustomerCreationView.
    :vartype template_name: str
    """
    form_class = CustomerCreationForm
    template_name = 'users/customer_form.html'


class UserUpdateView(UserPassesTestMixin, generic.edit.UpdateView):
    """
    This class handles user profile update requests.

    :ivar model: Base model of UserUpdateView.
    :vartype model: django.db.models.Model

    :ivar fields: Name of the fields to allow change from the user.
    :vartype fields: list

    :ivar template_name: Name of the template to render UserUpdateView.
    :vartype template_name: str
    """

    def test_func(self):
        """
        Function for checking access permission of requesting user to this view.

        :return: Return true if user passes test.
        :rtype: bool
        """
        return True

    model = User
    fields = ['username', 'first_name', 'last_name', 'email', ]
    template_name = 'users/customer_update.html'


class CustomerUpdateView(UserPassesTestMixin, generic.edit.UpdateView):
    """
    This class handles customer profile update requests.

    :ivar model: Base model of CustomerUpdateView.
    :vartype model: django.db.models.Model

    :ivar fields: Name of the fields to allow change from the customer.
    :vartype fields: list

    :ivar template_name: Name of the template to render CustomerUpdateView.
    :vartype template_name: str
    """

    def test_func(self):
        """
        Function for checking access permission of requesting user to this view.

        :return: Return true if user passes test.
        :rtype: bool
        """
        return True

    model = Customer
    fields = ['first_name', 'last_name', 'phone', ]
    template_name = 'users/customer_update.html'


class CustomerDeleteView(UserPassesTestMixin, generic.edit.DeleteView):
    """
    This class handles customer profile delete requests.

    :ivar model: Base model for CustomerDeleteView.
    :vartype model: django.db.models.Model
    """

    def test_func(self):
        """
        Function for checking access permission of requesting user to this view.

        :return: Return true if user passes test.
        :rtype: bool
        """
        return True

    model = Customer
