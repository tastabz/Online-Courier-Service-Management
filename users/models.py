from django.contrib.auth.models import User
from django.db import models
from django.shortcuts import reverse

# Create your models here.

"""List of users models."""


class Customer(User):
    """
    Customer model for creating customer instance in database.

    :ivar phone: Phone number of the customer.
    :vartype: django.db.models.CharField
    """
    phone = models.CharField(max_length=20, default=None)
    User._meta.get_field('email')._unique = True

    def get_absolute_url(self):
        """
        Function for getting absolute url for customer objects.

        :return: Absolute url of customer objects.
        :rtype: django.shortcuts.reverse
        """
        return reverse('users:customer_detail', kwargs={'pk': self.pk})

    # def save(self, *args, **kwargs):
    #     super(Customer, self).save(*args, **kwargs)

    class Meta:
        """
        Meta class of Customer model. Here you can declare metadata.

        :ivar verbose_name: Table name to show in the admin panel.
        :vartype verbose_name: str

        :ivar verbose_name_plural: Table name to show in the admin panel.
        :vartype verbose_name_plural: str
        """
        verbose_name = 'customer'
        verbose_name_plural = 'customers'


class DeliveryAgent(User):
    """
    DeliveryAgent model for creating delivery agent instance in database.

    :ivar phone: Phone number of the customer.
    :vartype: django.db.models.CharField
    """
    phone = models.CharField(max_length=20)
    User._meta.get_field('email')._unique = True

    # def save(self, *args, **kwargs):
    #     super(DeliveryAgent, self).save(*args, **kwargs)

    class Meta:
        """
        Meta class of DeliveryAgent model. Here you can declare metadata.

        :ivar verbose_name: Table name to show in the admin panel.
        :vartype verbose_name: str

        :ivar verbose_name_plural: Table name to show in the admin panel.
        :vartype verbose_name_plural: str
        """
        verbose_name = 'delivery agent'
        verbose_name_plural = 'delivery Agents'
