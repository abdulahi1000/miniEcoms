from django.db.models.signals import pre_save

from django.contrib.auth.models import User


def updataUser(sender, instance, **kwargs):
    user = instance
    if user.email != '':
        user.username = user.email
    print('signal Triggered')


pre_save.connect(updataUser, sender=User)
