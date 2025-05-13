from django.db import models
from django.db.models import F
from django.dispatch import receiver
from django.utils.timezone import now
from django.db.models.signals import pre_save, post_save, pre_delete
import os
from django.contrib.auth.models import AbstractUser


def get_upload_path(instance, filename):
    return os.path.join("documents", str(instance.owner.pk), str(filename))


class EncryptionKey(models.Model):
    key = models.CharField(max_length=64, null=False, blank=False)

    def __str__(self) -> str:
        return str(f"{self.key}")


class Year(models.Model):
    year = models.PositiveBigIntegerField(unique=True)

    def __str__(self) -> str:
        return str(self.year)


class Tribe(models.Model):
    name = models.CharField(
        max_length=50, unique=True, default=None, null=True, blank=True
    )

    def __str__(self) -> str:
        return str(self.name)


class HealthStatus(models.Model):
    name = models.CharField(
        max_length=50, unique=True, default=None, null=True, blank=True
    )

    def __str__(self) -> str:
        return str(self.name)


class Profession(models.Model):
    name = models.CharField(
        max_length=50, unique=True, default=None, null=True, blank=True
    )

    def __str__(self) -> str:
        return str(self.name)


class SocialStatus(models.Model):
    name = models.CharField(
        max_length=50, unique=True, default=None, null=True, blank=True
    )

    def __str__(self) -> str:
        return str(self.name)


class Handler(models.Model):
    lastName = models.CharField(max_length=50)
    firstName = models.CharField(max_length=50)
    day_of_birth = models.DateField(null=True, blank=True)
    type = models.CharField(max_length=20)
    phoneNumber = models.CharField(max_length=15, null=True, blank=True)

    def __str__(self):
        return str(f"{self.lastName} {self.firstName}")

    @property
    def age(self, *args, **kwargs):
        dob = self.day_of_birth
        return now().year - dob.year

    @property
    def fullName(self, *args, **kwargs):
        return self.__str__()


class Family(models.Model):
    year = models.ForeignKey(Year, on_delete=models.CASCADE)
    tribe = models.ForeignKey(
        Tribe, on_delete=models.SET_NULL, null=True, blank=True, default=None
    )
    lastName = models.CharField(max_length=50)
    firstName = models.CharField(max_length=50)
    father = models.CharField(max_length=50, null=True, blank=True)
    grandFather = models.CharField(max_length=50, null=True, blank=True)
    day_of_birth = models.DateField(default=now)
    idNumber = models.CharField(max_length=50, null=True, blank=True)
    healthStatus = models.ForeignKey(
        HealthStatus, on_delete=models.SET_NULL, null=True, blank=True, default=None
    )
    socialStatus = models.ForeignKey(
        SocialStatus, on_delete=models.SET_NULL, null=True, blank=True, default=None
    )
    profession = models.ForeignKey(
        Profession, on_delete=models.SET_NULL, null=True, blank=True, default=None
    )
    phoneNumber1 = models.CharField(max_length=15, null=True, blank=True)
    phoneNumber2 = models.CharField(max_length=15, null=True, blank=True)
    address = models.CharField(max_length=50, null=True, blank=True)
    email = models.CharField(max_length=50, null=True, blank=True)
    barcode = models.CharField(max_length=20, null=True, blank=True)
    handler = models.ForeignKey(
        Handler, on_delete=models.SET_NULL, null=True, blank=True
    )

    def __str__(self) -> str:
        return str(f"{self.lastName} {self.firstName}")

    @property
    def fullName(self, *args, **kwargs):
        return self.__str__()

    @property
    def age(self):
        today = now().date()
        return (
            today.year
            - self.day_of_birth.year
            - int(
                (today.month, today.day)
                < (self.day_of_birth.month, self.day_of_birth.day)
            )
        )

    @property
    def numberOfPersonInCustody(self, *args, **kwargs):
        return self.personincustody_set.all().count()

    @property
    def spouces_count(self, *args, **kwargs):
        return self.spouces.all().count()

    @property
    def children_count(self, *args, **kwargs):
        return self.children.all().count()

    def generate_barcode_number(self):
        import random
        import barcode

        if not self.id:
            return None

        year_part = str(self.year.year)
        id_part = str(self.id).zfill(5)[:5]
        random_part = str(random.randint(0, 999)).zfill(3)

        base_number = year_part + id_part + random_part

        ean = barcode.get_barcode_class("ean13")
        ean_code = ean(base_number)

        return ean_code.get_fullcode()


@receiver(post_save, sender=Family)
def generate_barcode_on_save(sender, instance: Family, created, **kwargs):

    if created and not instance.barcode:
        instance.barcode = instance.generate_barcode_number()
        instance.save()


class Document(models.Model):
    class DocumentsTypes(models.TextChoices):
        PROFILE_PIC = "profile-pic"
        OTHER = "other"

    owner = models.ForeignKey(Family, on_delete=models.CASCADE, related_name="files")
    file = models.FileField(upload_to=get_upload_path)
    # name = models.CharField(max_length=50)
    # type = models.CharField(max_length=20, null=True, choices=DocumentsTypes.choices)
    description = models.TextField(null=True, blank=True)
    date = models.DateField(auto_now_add=True)

    def __str__(self):
        return self.file.__str__()


class Child(models.Model):
    firstName = models.CharField(max_length=50)
    day_of_birth = models.DateField(default=now)
    gender = models.CharField(max_length=20)
    mother = models.CharField(max_length=50, null=True, blank=True)
    healthStatus = models.ForeignKey(
        HealthStatus, on_delete=models.SET_NULL, null=True, blank=True, default=None
    )
    notes = models.TextField(null=True, blank=True)
    family = models.ForeignKey(
        Family, on_delete=models.CASCADE, related_name="children"
    )

    def __str__(self) -> str:
        return str(f"{self.family.lastName} {self.firstName}")

    @property
    def age(self):
        today = now().date()
        return (
            today.year
            - self.day_of_birth.year
            - int(
                (today.month, today.day)
                < (self.day_of_birth.month, self.day_of_birth.day)
            )
        )

    @property
    def fullName(self, *args, **kwargs):
        return self.__str__()


class PersonInCustody(models.Model):
    firstName = models.CharField(max_length=50)
    lastName = models.CharField(max_length=50)
    day_of_birth = models.DateField(default=now)
    gender = models.CharField(max_length=20, null=True, blank=True)
    relation = models.CharField(max_length=50, null=True, blank=True)
    healthStatus = models.ForeignKey(
        HealthStatus, on_delete=models.SET_NULL, null=True, blank=True, default=None
    )
    notes = models.TextField(null=True, blank=True)
    family = models.ForeignKey(Family, on_delete=models.CASCADE)

    def __str__(self) -> str:
        return str(f"{self.lastName} {self.firstName}")

    @property
    def fullName(self, *args, **kwargs):
        return self.__str__()

    @property
    def age(self, *args, **kwargs):
        dob = self.day_of_birth
        return now().year - dob.year


class Spouce(models.Model):
    firstName = models.CharField(max_length=50)
    lastName = models.CharField(max_length=50)
    day_of_birth = models.DateField(default=now)
    healthStatus = models.ForeignKey(
        HealthStatus, on_delete=models.SET_NULL, null=True, blank=True, default=None
    )
    notes = models.TextField(null=True, blank=True)
    family = models.ForeignKey(Family, on_delete=models.CASCADE, related_name="spouces")

    def __str__(self) -> str:
        return str(f"{self.lastName} {self.firstName}")

    @property
    def fullName(self, *args, **kwargs):
        return self.__str__()

    @property
    def age(self, *args, **kwargs):
        dob = self.day_of_birth
        return now().year - dob.year


class Product(models.Model):
    category = models.CharField(max_length=50)
    type = models.CharField(max_length=50)
    quantity = models.PositiveIntegerField(null=True, blank=True, default=0)

    def __str__(self) -> str:
        return str(f"{self.category} - {self.type}")


class Donation(models.Model):
    donor = models.CharField(max_length=50, null=True, blank=True)
    product = models.ForeignKey(Product, on_delete=models.SET_NULL, null=True)
    date = models.DateField(null=True, blank=True)
    quantity = models.PositiveIntegerField()

    def __str__(self) -> str:
        return str(f"{self.product} : {self.date}")


class Delivery(models.Model):
    occasion = models.CharField(max_length=50, null=True, blank=True)
    date = models.DateField()
    quantity = models.PositiveIntegerField()
    beneficiary = models.ForeignKey(Family, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)

    def __str__(self) -> str:
        return str(f"{self.beneficiary} : {self.product} - {self.date}")


@receiver(pre_save, sender=Donation)
def capture_previous_Donation_state(sender, instance, **kwargs):

    if instance.pk:  # Only for updates
        instance._previous_Donation = Donation.objects.select_related("product").get(
            pk=instance.pk
        )


@receiver(post_save, sender=Donation)
def update_product_quantity(sender, instance, created, **kwargs):
    """
    Adjust product quantities when a Donation is created or updated.
    Handles product changes during updates.
    """
    if created:
        # On creation, deduct the Donation quantity from the product
        instance.product.quantity = F("quantity") + instance.quantity
        instance.product.save()
    else:
        # On update, check the previous state
        previous_Donation = getattr(instance, "_previous_Donation", None)
        if previous_Donation:
            # Handle product change
            if previous_Donation.product != instance.product:
                # Restore quantity to the old product
                previous_Donation.product.quantity = (
                    F("quantity") - previous_Donation.quantity
                )
                previous_Donation.product.save()

                # Deduct quantity from the new product
                instance.product.quantity = F("quantity") + instance.quantity
                instance.product.save()
            else:
                # Adjust quantity for the same product
                adjustment = instance.quantity - previous_Donation.quantity
                instance.product.quantity = F("quantity") + adjustment
                instance.product.save()


@receiver(pre_delete, sender=Donation)
def handle_Donation_delete(sender, instance, **kwargs):
    """
    Revert the product quantity when a Donation is deleted.
    """
    instance.product.quantity = F("quantity") - instance.quantity
    instance.product.save()


@receiver(pre_save, sender=Delivery)
def capture_previous_delivery_state(sender, instance, **kwargs):
    """
    Capture the previous state of the Delivery object before saving.
    This is used to handle updates.
    """
    if instance.pk:  # Only for updates
        instance._previous_delivery = Delivery.objects.select_related("product").get(
            pk=instance.pk
        )


@receiver(post_save, sender=Delivery)
def update_product_quantity(sender, instance, created, **kwargs):
    """
    Adjust product quantities when a delivery is created or updated.
    Handles product changes during updates.
    """
    if created:
        # On creation, deduct the delivery quantity from the product
        instance.product.quantity = F("quantity") - instance.quantity
        instance.product.save()
    else:
        # On update, check the previous state
        previous_delivery = getattr(instance, "_previous_delivery", None)
        if previous_delivery:
            # Handle product change
            if previous_delivery.product != instance.product:
                # Restore quantity to the old product
                previous_delivery.product.quantity = (
                    F("quantity") + previous_delivery.quantity
                )
                previous_delivery.product.save()

                # Deduct quantity from the new product
                instance.product.quantity = F("quantity") - instance.quantity
                instance.product.save()
            else:
                # Adjust quantity for the same product
                adjustment = instance.quantity - previous_delivery.quantity
                instance.product.quantity = F("quantity") - adjustment
                instance.product.save()


@receiver(pre_delete, sender=Delivery)
def handle_delivery_delete(sender, instance, **kwargs):
    """
    Revert the product quantity when a delivery is deleted.
    """
    instance.product.quantity = F("quantity") + instance.quantity
    instance.product.save()
