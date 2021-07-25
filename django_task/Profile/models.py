from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils.translation import gettext_lazy as _


class Profile(AbstractUser):
    """
        Inherit Django User all fields and  add custom fields
    """
    GENDER_TYPE_CHOICES = (
        ('M', _("Male")),
        ('F', _("Female")),
        ('OTHERS', _("Others")),
    )
    phone_number = models.CharField(unique=True, max_length=100)
    gender = models.CharField(
        max_length=100,
        choices=GENDER_TYPE_CHOICES,
        blank=True,
        null=True
    )
    pic = models.FileField(upload_to='images/', blank=True, null=True)
    dob = models.DateField(blank=True, null=True)
    permanent_address = models.OneToOneField(
        'Profile.Address',
        related_name='permanent_address',
        on_delete=models.PROTECT, 
        blank=True, 
        null=True
    )
    company_address = models.OneToOneField(
        'Profile.Address',
        related_name='company_address',
        on_delete=models.PROTECT, 
        blank=True, 
        null=True
    )
    friends = models.ManyToManyField("self", blank=True)
    email = models.EmailField(_('email address'), blank=False)

    # USERNAME_FIELD = 'phone_number'
    # objects = ProfileManager()

    class Meta:
        ordering = ['dob']
    
    def __str__(self):
        return str(self.phone_number)


class Address(models.Model):
    """
        Address Model 
    """
    id = models.BigAutoField(primary_key=True)
    street = models.CharField(max_length=100)
    city = models.CharField(max_length=100)
    state = models.CharField(max_length=100)
    pincode = models.CharField(max_length=100)
    country = models.CharField(max_length=100)

    class Meta:
        managed = True

    def __str__(self):
        return str(self.id)
