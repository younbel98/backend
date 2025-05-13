from django.conf import settings
from django.db.models.signals import post_save, post_migrate
from django.dispatch import receiver
from rest_framework.authtoken.models import Token
from api.models import Year, HealthStatus, Profession, SocialStatus, Tribe, EncryptionKey
from django.utils.timezone import now



@receiver(post_migrate)
def insert_initial_data(sender, **kwargs):
    if sender.name == "api":
        EncryptionKey.objects.get_or_create(key='1sWm8XkhXcK7qP8HkG3Fy1ZC4eOQWTrqP89xQ1UymXQ=')
        Year.objects.get_or_create(year = now().date().year)
        createHealthStatus()
        createSocialStatus()
        createProfessions()
        createTribes()

def createTribes():
    tribes = ['لا يوجد']
    for item in tribes:
        Tribe.objects.get_or_create(name=item)

def createHealthStatus():
    healthStatus = ['لا يوجد', 'مرض مزمن', 'إعاقة']
    for item in healthStatus:
        HealthStatus.objects.get_or_create(name=item)

def createSocialStatus():
    socialStatus = ['لا يوجد', 'مطلقة', 'معلقة', 'أرملة', 'دخل ضعيف']
    for item in socialStatus:
        SocialStatus.objects.get_or_create(name=item)

def createProfessions():
    professions = ['لا يوجد', 'عامل يومي', 'بدون دخل', 'عامل يومي']
    for item in professions:
        Profession.objects.get_or_create(name=item)


@receiver(post_save, sender=settings.AUTH_USER_MODEL)
def create_auth_token(sender, instance=None, created=False, **kwargs):
    if created:
        Token.objects.create(user=instance)