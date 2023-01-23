# if you want create custom models these all steps are mandatory so be careful to do
# These all are not remembered so better to go Django Documentation custom models

from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager
# Create your models here.

class MyAccountManager(BaseUserManager):
    def create_user(self, first_name, last_name, user_name, email, password=None):
        if not email:
            raise ValueError('User must have an email address')

        if not user_name:
            raise ValueError("User must have an username")

        user = self.model(
            email = self.normalize_email(email), #here normalize_email means user give any capital letter in email normalize_email automatically take small lette only
            user_name = user_name,
            first_name = first_name,
            last_name = last_name,
        )

        user.set_password(password)
        user.save(using=self.db)
        return user

    def create_superuser(self, first_name, last_name, user_name, email, password=None):
        user = self.create_user(
            email = self.normalize_email(email),
            user_name = user_name,
            password = password,
            first_name = first_name,
            last_name = last_name,
        )
        user.is_admin = True
        user.is_staff = True
        user.is_active = True
        user.is_superadmin = True
        user.save(using=self.db)
        return user



# These all are steps are mandatory
class Account(AbstractBaseUser):
    first_name  =   models.CharField(max_length=50)
    last_name  =   models.CharField(max_length=50)
    user_name  =   models.CharField(max_length=50, unique=True)
    email  =   models.EmailField(max_length=100, unique=True)
    phone_number    =   models.CharField(max_length=50)

    #require
    date_joined  = models.DateField(auto_now_add=True)
    last_login  = models.DateField(auto_now_add=True)
    is_admin  = models.BooleanField(default=False)
    is_staff  = models.BooleanField(default=False)
    is_active  = models.BooleanField(default=False)
    is_superadmin  = models.BooleanField(default=False)


    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['user_name','first_name','last_name']

    objects = MyAccountManager()

    def full_name(self):
        return f' {self.first_name} {self.last_name} '

    def __str__(self):
        return self.email

    def has_perm(self,perm,obj=None):  #perm = permission
        return self.is_admin

    def has_module_perms(self,add_label):
        return True

class UserProfile(models.Model):
    user = models.OneToOneField(Account,on_delete=models.CASCADE)
    address_line_1 = models.CharField(blank=True, max_length=100)
    address_line_2 = models.CharField(blank=True, max_length=100)
    profile_picture = models.ImageField(blank=True,upload_to='userprofile')
    city = models.CharField(blank=True,max_length=25)
    state = models.CharField(blank=True,max_length=25)
    country = models.CharField(blank=True,max_length=25)

    def __str__(self):
        return self.user.first_name
    def full_address(self):
        return f'{self.address_line_1} {self.address_line_2}'
