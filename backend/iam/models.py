from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from django.utils import timezone
from django.db import models

class User(models.Model):
    USER_TYPES = [
        ('SuperAdmin', 'SuperAdmin'),
        ('SubAdmin', 'SubAdmin'),
        ('User', 'User'),
        ('CSRAgent', 'CSRAgent'),
        ('DWAdmin', 'DWAdmin'),
        ('DWAgent', 'DWAgent'),
        ('MasterExternalAgent', 'MasterExternalAgent'),
        ('ExternalAgent', 'ExternalAgent'),
    ]

    STATUS_CHOICES = [
        ('Pending', 'Pending'),
        ('Confirmed', 'Confirmed'),
        ('Rejected', 'Rejected'),
    ]

    BLOCK_USER_CHOICES = [
        ('0', 'Active'),
        ('1', 'Blocked'),
    ]

    id = models.BigAutoField(primary_key=True)
    balance = models.DecimalField(max_digits=50, decimal_places=2, default=0.00)
    bonus_won = models.DecimalField(max_digits=38, decimal_places=2, default=0.00)
    name = models.CharField(max_length=100)
    first_name = models.CharField(max_length=191, null=True, blank=True)
    last_name = models.CharField(max_length=191, null=True, blank=True)
    dob = models.DateField(null=True, blank=True)
    email = models.CharField(max_length=191, null=True, blank=True)
    unique_id = models.CharField(max_length=100, null=True, blank=True)
    referrer_code = models.CharField(max_length=100, null=True, blank=True)
    referred_by = models.CharField(max_length=191, null=True, blank=True)
    phone_code = models.CharField(max_length=100, null=True, blank=True)
    mobile = models.CharField(max_length=100, null=True, blank=True)
    currency = models.CharField(max_length=191, null=True, blank=True)
    info = models.CharField(max_length=191, null=True, blank=True)
    token = models.CharField(max_length=191, null=True, blank=True)
    new_token = models.CharField(max_length=191, null=True, blank=True)
    user_type = models.CharField(max_length=50, choices=USER_TYPES, default='User')
    reg_type = models.CharField(max_length=191)
    block_user = models.CharField(max_length=1, choices=BLOCK_USER_CHOICES, default='0')
    otp = models.IntegerField(default=0)
    otp_verify = models.IntegerField(null=True, blank=True)
    password = models.CharField(max_length=191, null=True, blank=True)
    designation_id = models.CharField(max_length=10000, default='0')
    admin_id = models.CharField(max_length=11, null=True, blank=True)
    agent_id = models.IntegerField(null=True, blank=True)
    agent_password = models.CharField(max_length=191, null=True, blank=True)
    remember_token = models.CharField(max_length=100, null=True, blank=True)
    profileimage = models.CharField(max_length=100, null=True, blank=True)
    telegram = models.CharField(max_length=191, null=True, blank=True)
    instagram = models.CharField(max_length=191, null=True, blank=True)
    whatsapp_no = models.CharField(max_length=191, null=True, blank=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='Pending')
    enteredbyid = models.CharField(max_length=100, null=True, blank=True)
    remark = models.TextField(null=True, blank=True)
    is_added_back_office = models.IntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    deleted_at = models.DateTimeField(null=True, blank=True)
    updated_at = models.DateTimeField(auto_now=True)
    password_changed_at = models.DateTimeField(null=True, blank=True)
    extra_info = models.CharField(max_length=255, null=True, blank=True)
    master_external_agent_id = models.CharField(max_length=255, null=True, blank=True)

    class Meta:
        db_table = 'users'
        verbose_name = 'User'
        verbose_name_plural = 'Users'

    def __str__(self):
        return self.name


class ActiveToken(models.Model):
    user = models.ForeignKey('User', on_delete=models.CASCADE, related_name='active_tokens')
    jti = models.CharField(max_length=255, unique=True)        # JWT ID
    token_type = models.CharField(max_length=10)               # access / refresh
    expires_at = models.DateTimeField()
    created_at = models.DateTimeField(default=timezone.now)

    class Meta:
        db_table = 'active_tokens'


class BlacklistedToken(models.Model):
    user_id = models.BigIntegerField(null=True, blank=True)
    jti = models.CharField(max_length=255, unique=True)
    token_type = models.CharField(max_length=10)
    revoked_at = models.DateTimeField(default=timezone.now)
    expires_at = models.DateTimeField(null=True, blank=True)

    class Meta:
        db_table = 'blacklisted_tokens'
