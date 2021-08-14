from django.contrib.auth.models import User
from django.db import models
from django.utils.safestring import mark_safe


from django.db.models.signals import post_save
from django.dispatch import receiver

from django.forms import ModelForm

class UserProfile(models.Model):
    GENDER = (
        ('Male', 'Male'),
        ('Female', 'Female'),
        ('Other', 'Other'),
    )

    user = models.OneToOneField(User, on_delete=models.CASCADE)
    # first_name = models.ForeignKey(username.first_name, on_delete=models.CASCADE)
    # last_name = models.ForeignKey(User.last_name, on_delete=models.CASCADE)
    # email = models.ForeignKey(User.email, on_delete=models.CASCADE)

    phone = models.CharField(blank=True, max_length=20)
    address = models.CharField(blank=True, max_length=150)
    city = models.CharField(blank=True, max_length=20)
    country = models.CharField(blank=True, max_length=20)
    image = models.ImageField(blank=True)
    language = models.CharField(blank=True, max_length=20)
    gender = models.CharField(max_length=10, choices=GENDER,default="Other")
    signup_confirmation = models.BooleanField(default=False)
    def __str__(self):
        return self.user.username

    def user_name(self):
        return self.user.first_name + ' ' + self.user.last_name + ' [' + self.user.username + '] '

@receiver(post_save, sender=User)
def update_profile_signal(sender, instance, created, **kwargs):
    for user in User.objects.all():
        if hasattr(user,'userprofile') and not user.userprofile:
            UserProfile.objects.create(user=instance)
            instance.userprofile.save()