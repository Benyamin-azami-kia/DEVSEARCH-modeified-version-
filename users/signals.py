from django.db.models.signals import post_delete, post_save
from django.core.mail import send_mail
from django.contrib.auth.models import User
from django.dispatch import receiver
from .models import Profile


@receiver(post_save, sender=User)
def create_profile(sender, instance, created, **kwargs):
    user=instance
    if created:
        Profile.objects.create(
            user=user
        )

        subject='DevSearch Registration'
        message=f'Welcom {user.username} to DevSearch'
        from_email='devsearchmail.gmail.com'

        send_mail(subject=subject,
                    message=message,
                    from_email=from_email,
                    recipient_list=[user.email])


@receiver(post_delete, sender=Profile)
def delete_user(sender, instance, **kwargs):
    instance.user.delete()


@receiver(post_save, sender=Profile)
def update_profile(sender, instance, created, **kwargs):
    profile=instance
    if not created:
        if profile.profile_image =='':
            profile.profile_image='profiles/user-default.png'
            profile.save()