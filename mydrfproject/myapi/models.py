from django.contrib.auth.models import AbstractUser
from django.db import models

from django.core.mail import send_mail
from django.dispatch import receiver
from django.template.loader import render_to_string
from django.urls import reverse
from django_rest_passwordreset.signals import reset_password_token_created

class CustomUser(AbstractUser):
    email = models.EmailField(unique=True)

    first_name = models.CharField(max_length=30, blank=True)
    last_name = models.CharField(max_length=30, blank=True)
    age = models.PositiveIntegerField(blank=True, null=True)
    country = models.CharField(max_length=100, blank=True)
    residence = models.CharField(max_length=100, blank=True)


    def __str__(self):
        return self.username


@receiver(reset_password_token_created)
def password_reset_token_created(sender, instance, reset_password_token, *args, **kwargs):
    email_plaintext_message = "{}?token={}".format(reverse('password_reset:reset-password-request'), reset_password_token.key)
    send_mail(
        "Password Reset for Your Account",
           email_plaintext_message,
        "from@example.com",
    [reset_password_token.user.email],
    )

class ProgrammingLanguage(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    level = models.CharField(max_length=20)  # beginner, experienced, expert

class Project(models.Model):
    creator = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    project_name = models.CharField(max_length=100)
    description = models.TextField()
    maximum_collaborators = models.PositiveIntegerField()
    collaborators = models.ManyToManyField(CustomUser, related_name='projects')

class Collaboration(models.Model):
    project = models.ForeignKey(Project, on_delete=models.CASCADE)
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    accepted = models.BooleanField(default=False)

class Skill(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    proficiency = models.CharField(max_length=20)  # e.g., beginner, intermediate, advanced

    def __str__(self):
        return self.name    