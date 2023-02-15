from django.contrib.auth.models import User
from django.db import models
from django.shortcuts import reverse

from users.models import Customer, DeliveryAgent


# Create your models here.

"""List of parcels model."""


class Address(models.Model):
    """
    Address model for creating address instance in database.

    :ivar country:
    :vartype country: django.db.models.CharField

    :ivar city:
    :vartype city: django.db.models.CharField

    :ivar street:
    :vartype street: django.db.models.CharField

    :ivar zip:
    :vartype zip: django.db.models.CharField
    """
    country = models.CharField(max_length=20)
    city = models.CharField(max_length=20)
    street = models.CharField(max_length=20)
    zip = models.CharField(max_length=20)

    def save(self, *args, **kwargs):
        """
        This funtcion will be called on address instance save.

        :param args: Arguments data.
        :param kwargs: Kwargs data.
        :return: None
        """
        super(Address, self).save(*args, **kwargs)


class Receiver(models.Model):
    """
    Receiver model for creating receiver instance in database.

    :ivar name: Receiver name.
    :vartype name: django.db.models.CharField

    :ivar email: Receiver email.
    :vartype email: django.db.models.EmailField

    :ivar phone: Receiver phone.
    :vartype phone: django.db.models.CharField

    :ivar address: Receiver address.
    :vartype address: Address
    """
    name = models.CharField(max_length=100)
    email = models.EmailField()
    phone = models.CharField(max_length=20)
    address = models.OneToOneField(Address, on_delete=models.CASCADE)

    def save(self, *args, **kwargs):
        """
        This function will be called on receiver instance save.

        :param args: Arguments data.
        :param kwargs: Kwargs data.
        :return: None
        """
        super(Receiver, self).save(*args, **kwargs)


class Parcel(models.Model):
    """
    Parcel model for creating parcel instance in database.

    :ivar title: Parcel title.
    :vartype title: django.db.models.CharField

    :ivar type: Parcel type.
    :vartype type: django.db.models.CharField

    :ivar status: Parcel status.
    :vartype status: django.db.models.CharField

    :ivar pickup_address: Parcel pickup-address.
    :vartype pickup_address: Address

    :ivar receiver: Parcel receiver.
    :vartype receiver: Receiver

    :ivar booked_on: Parcel booking time.
    :vartype booked_on: django.db.models.DateTimeField

    :ivar booked_by: Parcel creator.
    :vartype booked_by: Customer

    :ivar delivery_agent: Parcel delivery-agent.
    :vartype delivery_agent: DeliveryAgent
    """

    TYPE = [
        ('money', 'Money'),
        ('fruits', 'Fruits'),
        ('fragile', 'Fragile'),
        ('document', 'Document'),
        ('furniture', 'Furniture'),
        ('perishable', 'Perishable'),
        ('electronics', 'Electronics'),
    ]
    STATUS = [
        ('on_delivery', 'On Delivery'),
        ('processing', 'Processing'),
        ('delivered', 'Delivered'),
        ('pending', 'Pending'),
        ('picked', 'Picked'),
    ]
    title = models.CharField(max_length=100)
    type = models.CharField(max_length=20, choices=TYPE, blank=True)
    status = models.CharField(max_length=100, choices=STATUS, default='pending', blank=True)
    pickup_address = models.OneToOneField(Address, on_delete=models.CASCADE)
    receiver = models.OneToOneField(Receiver, on_delete=models.CASCADE)
    booked_on = models.DateTimeField(auto_now_add=True, editable=False)
    booked_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name='booked_by', editable=False)
    delivery_agent = models.ForeignKey(DeliveryAgent, blank=True, on_delete=models.CASCADE)

    def get_absolute_url(self):
        """
        Function to get absolute url of parcel objects.

        :return: Absolute url of the instance.
        :rtype: django.shortcuts.reverse
        """

        return reverse('parcels:detail', kwargs={'pk': self.pk})

    def __str__(self):
        return str(self.pk)

    def save(self, *args, **kwargs):
        """
        This function will be called on parcel instance save.

        :param args: Arguments data.
        :param kwargs: Kwargs data.
        :return: void
        """
        super(Parcel, self).save(*args, **kwargs)


class Issue(models.Model):
    """
    Issue model for creating issue instance in database.

    :ivar category: Issue category.
    :vartype category: django.db.models.CharField

    :ivar status: Issue status.
    :vartype status: django.db.models.CharField

    :ivar message: Issue description.
    :vartype message: django.db.models.CharField

    :ivar reply: Reply from admin.
    :vartype reply: django.db.models.CharField

    :ivar parcel: Issue created for this parcel id.
    :vartype parcel: Parcel
    """

    CATEGORY = [
        ('delivery', 'Delivery'),
        ('product', 'Product'),
        ('delivery_agent', 'Delivery Agent')
    ]
    STATUS = [
        ('pending', 'Pending'),
        ('processing', 'Processing'),
        ('solved', 'Solved'),
    ]
    category = models.CharField(max_length=20, choices=CATEGORY, blank=True)
    status = models.CharField(max_length=20, choices=STATUS, blank=True)
    message = models.CharField(max_length=1000)
    reply = models.CharField(max_length=1000, blank=True)
    parcel = models.ForeignKey(Parcel, on_delete=models.CASCADE)

    def save(self, *args, **kwargs):
        """
        This function will be called on issue instance save.

        :param args: Arguments data.
        :param kwargs: Kwargs data.
        :return: void
        """
        super(Issue, self).save(*args, **kwargs)
