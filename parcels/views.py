from decouple import config
from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.core.mail import send_mail
from django.shortcuts import redirect, render
from django.views.generic import DetailView, ListView, FormView
from django.views.generic.edit import CreateView, UpdateView, DeleteView

from .forms import ParcelTrackForm, CostCalculatorForm, AddressForm, ReceiverForm, ParcelForm
from .models import Parcel, Address, Issue


# Create your views here.

"""List of parcels views"""


class CostCalculatorView(FormView):
    form_class = CostCalculatorForm
    template_name = 'parcels/cost_calculator.html'

    def post(self, request, *args, **kwargs):
        if request.POST['weight'] == '0':
            messages.error(request, 'Weight cannot be 0')
            return redirect('parcels:cost_calculator')
        unit_price = 15.0
        minimum_cost = 60.0
        if request.POST['area'] == 'outside':
            unit_price = 30.0
            minimum_cost = 120.0

        charge = max(minimum_cost, unit_price * float(request.POST['weight']))
        messages.success(request, f'Estimated shipping cost is {charge} taka')
        return redirect('parcels:cost_calculator')


class ParcelListView(LoginRequiredMixin, ListView):
    """This class handles parcel list view requests from the customers."""

    def get_queryset(self):
        """
        This function retrieve objects from database by query.

        :return: list of parcel objects placed by the requesting user.
        :rtype: list
        """
        return Parcel.objects.filter(booked_by=self.request.user)


class ParcelDetailView(DetailView):
    """
    This class handles parcel detail view requests from the customers.

    :ivar model: Base model of ParcelDetailView.
    :vartype model: django.db.models.Model
    """
    model = Parcel

    def get(self, request, *args, **kwargs):
        """
        This function will be called on get request of ParcelDetailVIew.

        :param request: Type of request from the customers.
        :param args: Holds other values.
        :param kwargs: Holds other values.
        :return: Return render template view.
        :rtype: django.shortcuts.render
        """
        self.object = self.get_object()
        context = self.get_context_data(object=self.object)
        return render(request, 'parcels/' + self.object.status + '.html', context)


class ParcelCreateView(LoginRequiredMixin, CreateView):
    """
    This class handles parcel create requests from the customers.

    :ivar model: Base model of ParcelCreateView.
    :vartype model: django.db.models.Model

    :ivar fields: Name of the fields needs to provide to create a parcel.
    :vartype fields: list

    :ivar template_name: Name of the template to render ParcelCreateView.
    :vartype template_name: str
    """
    model = Parcel
    fields = ['title', 'type', ]
    template_name = 'parcels/parcel_form.html'

    def get(self, request, *args, **kwargs):
        """
        This function will be called on get request of ParcelCreateView.

        :param request: Request data from the user.
        :param args: Holds other arguments values.
        :param kwargs: Holds kwargs values.

        :ivar parcel_form: Form to fill about parcel information.
        :vartype parcel_form: django.forms.Form

        :ivar pickup_address_form: Form to fill about pickup address information.
        :vartype pickup_address_form: django.forms.Form

        :ivar receiver_form: Form to fill about receiver information.
        :vartype receiver_form: django.forms.Form

        :ivar receiver_address_form: Form to fill about receiver address information.
        :vartype receiver_address_form: django.forms.Form

        :ivar context: Context data to return.
        :vartype context: dict

        :return: Render template view.
        :rtype: django.shortcuts.render
        """
        parcel_form = self.get_form()
        pickup_address_form = AddressForm()
        receiver_form = ReceiverForm()
        receiver_address_form = AddressForm()
        context = {
            'parcel_form': parcel_form,
            'pickup_address_form': pickup_address_form,
            'receiver_form': receiver_form,
            'receiver_address_form': receiver_address_form,
        }
        return render(request=request, template_name=self.get_template_names(), context=context)

    def post(self, request, *args, **kwargs):
        """
        This function will be called on post request of ParcelCreateView.

        :param request: Request data from the user.
        :param args: Holds other arguments values.
        :param kwargs: Holds kwargs values.

        :ivar parcel: Parcel object, created from the data provided by the customer in parcel_form.
        :vartype parcel: Prcel

        :ivar pickup_address: Parcel pickup address, object created from the data provided by the customer in pickup_address_form.
        :vartype pickup_address: Address

        :ivar receiver: Receiver of the parcel, object created from the data provided by the customer in receiver_form.
        :vartype receiver: Receiver

        :ivar receiver_address: Parcel receivers address,  object created from the data provided by the customer in receiver_address_form.
        :vartype receiver_address: Address

        :ivar sender_message: Message to send to sender on parcel creation.
        :vartype sender_message: str

        :ivar receiver_message: Message to send to receiver on parcel creation.
        :vartype receiver_message: str

        :return: Render template view.
        :rtype: django.shortcuts.redirect
        """
        parcel = ParcelForm(request.POST).save()
        pickup_address = Address(country=request.POST.getlist('country')[0], city=request.POST.getlist('city')[0],
                                 street=request.POST.getlist('street')[0], zip=request.POST.getlist('zip')[0])
        pickup_address.save()
        receiver_address = Address(country=request.POST.getlist('country')[1], city=request.POST.getlist('city')[1],
                                   street=request.POST.getlist('street')[1], zip=request.POST.getlist('zip')[1])
        receiver_address.save()

        receiver = ReceiverForm(request.POST).save()
        receiver.address = receiver_address
        receiver.save()
        parcel.pickup_address = pickup_address
        parcel.receiver = receiver
        parcel.booked_by = request.user
        parcel.save()
        messages.success(request, 'Your parcel has been placed successfully')

        sender_message = "You are receiving this email because you have placed a new parcel at "
        receiver_message = "You are receiving this email because a new parcel has been placed for your at "

        message = f"{request.META['HTTP_HOST']}. Please visit our website to know more." + \
                  f"\n\nYour parcel tracking ID: {parcel.id}" + \
                  f"\n\nThanks for using our service!" + \
                  f"\n\nThe {request.META['HTTP_HOST']} team"

        send_mail(
            subject='New Parcel',
            message=sender_message + message,
            from_email=config('EMAIL'),
            recipient_list=[parcel.booked_by.email],
        )

        send_mail(
            subject='New Parcel',
            message=receiver_message + message,
            from_email=config('EMAIL'),
            recipient_list=[parcel.receiver.email],
        )

        return redirect('parcels:list')


class ParcelUpdateView(UserPassesTestMixin, UpdateView):
    """
    This class handles parcel update requests from customers.

    :ivar model: Base model of ParcelUpdateView.
    :vartype model: django.db.models.Model

    :ivar fields: Name of the fields of parcel to allow change from the customers.
    :vartype fields: list

    :ivar template_name: Name of the template to render ParcelUpdateView.
    :vartype template_name: str
    """

    def test_func(self):
        """
        Function for checking access permission of requesting user to this view.

        :return: Return true if user passes test.
        :rtype: bool
        """
        return self.request.user == self.get_object().booked_by

    model = Parcel
    fields = ['type', 'city', 'street', 'zip', 'email', 'phone', ]
    template_name = 'parcels/parcel_update.html'


class ParcelDeleteView(UserPassesTestMixin, DeleteView):
    """
    This class handles parcel delete requests from customers.

    :ivar model: Base model of ParcelDeleteView.
    :vartype model: django.db.models.Model
    """

    def test_func(self):
        """
        Function for checking access permission of requesting user to this view.

        :return: Return true if user passes test.
        :rtype: bool
        """
        return self.request.user == self.get_object().booked_by

    model = Parcel
    # success_url = 'parcels:parcels'  # fixme: having trouble here for success url


class ParcelTrackView(FormView):
    """
    This class handles parcel track requests from customers.

    :ivar form_class: Form to fill to track parcel.
    :vartype form_class: django.forms.Form

    :ivar template_name: Name of the template to render ParcelTrackView.
    :vartype template_name: str
    """
    form_class = ParcelTrackForm
    template_name = 'parcels/parcel_track.html'

    def post(self, request, *args, **kwargs):
        """
        This function will be called on post request of ParcelTrackView.

        :param request: Request data from the user.
        :param args: Holds other arguments values.
        :param kwargs: Holds kwargs values.
        :return: Redirect to parcel urls.
        :rtype: django.shortcuts.redirect
        """
        try:
            parcel = Parcel.objects.get(pk=request.POST['parcel_id'])
            print(parcel)
            return redirect('parcels:detail', pk=parcel.pk)
        except Exception as e:
            print(str(e))
            messages.error(request, 'Invalid parcel ID')
            return redirect('parcels:track')


class IssueCreateView(CreateView):
    """
    This class handles issue create requests from customers.

    :ivar model: Base model of IssueCreateView.
    :vartype model: django.db.models.Model

    :ivar fields: Name of the fields to provide to create an issue.
    :vartype fields: list
    """
    model = Issue
    fields = ['category', 'message', ]

    def post(self, request, *args, **kwargs):
        """
        This function will be called on post request of IssueCreateView.

        :param request: Request data from the user.
        :param args: Holds other arguments values.
        :param kwargs: Holds kwargs values.
        :return: Redirect to parcels:list urls.
        :rtype: django.shortcuts.redirect
        """
        form = self.get_form()
        issue = form.save(self)
        issue.parcel = Parcel.objects.get(pk=kwargs['pk'])
        print(kwargs)
        issue.save()
        return redirect('parcels:list')
