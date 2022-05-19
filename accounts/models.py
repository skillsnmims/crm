from django.db import models
from django.contrib.auth.models import PermissionsMixin
from django.contrib.auth.base_user import AbstractBaseUser
from django.db.models.signals import post_delete

from .managers import UserManager


USER_TYPE_CHOICES = (("SA", "Super Admin"), ("BA", "Branch Admin"), ("QA", "Quality Assurance"), ("AG", "Agent"), ("VS", "Visitor"))


class User(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField('email address', unique=True)
    registered_on = models.DateTimeField('date joined', auto_now_add=True)
    user_type = models.CharField(max_length=2, choices=USER_TYPE_CHOICES)
    is_active = models.BooleanField('active', default=True)
    avatar = models.ImageField(upload_to='avatars/', null=True, blank=True)
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)

    objects = UserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    class Meta:
        verbose_name = 'user'
        verbose_name_plural = 'users'

    @property
    def is_super_admin(self):
        return self.user_type == "SA"

    @property
    def is_branch_admin(self):
        return self.user_type == "BA"

    @property
    def is_visitor(self):
        return self.user_type == "VS"

    @property
    def is_agent(self):
        return self.user_type == "AG"


    @property
    def get_branch(self):
        try:
            return self.branchadmin.branch
        except:
            return None

    @property
    def get_agent_name(self):
        if self.user_type == "AG":
            return self.agent.name
        else:
            return "N/A"


class BranchAdmin(models.Model):

    user = models.OneToOneField(User, on_delete=models.CASCADE)
    first_name = models.CharField(max_length=64)
    last_name = models.CharField(max_length=64)
    branch = models.ForeignKey("branches.Branch", on_delete=models.CASCADE)

    def __str__(self):
        return "{} {}".format(self.first_name, self.last_name)


def delete_user(sender, instance, *args, **kwargs):
    instance.user.delete()


post_delete.connect(delete_user, sender=BranchAdmin)


class QualityAgent(models.Model):

    user = models.OneToOneField(User, on_delete=models.CASCADE)
    first_name = models.CharField(max_length=64)
    last_name = models.CharField(max_length=64)
    branch = models.ForeignKey("branches.Branch", on_delete=models.CASCADE)
    campaign = models.ForeignKey("campaigns.Campaign", on_delete=models.CASCADE)

    def __str__(self):
        return "{} {}".format(self.first_name, self.last_name)


post_delete.connect(delete_user, sender=QualityAgent)


class Visitor(models.Model):

    user = models.OneToOneField(User, on_delete=models.CASCADE)
    first_name = models.CharField(max_length=64)
    last_name = models.CharField(max_length=64)
    branch = models.ForeignKey("branches.Branch", on_delete=models.CASCADE)

    def __str__(self):
        return "{} {}".format(self.first_name, self.last_name)


post_delete.connect(delete_user, sender=Visitor)
