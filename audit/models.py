from django.db import models
from django.contrib.auth.models import User


class IDC(models.Model):
    name = models.CharField(max_length=64, unique=True)

    def __str__(self):
        return self.name


class Host(models.Model):
    """
    host info
    """
    hostname = models.CharField(max_length=64, unique=True)
    ip_addr = models.GenericIPAddressField(unique=True)
    port = models.IntegerField(default=22)
    idc = models.ForeignKey("IDC")
    enabled = models.BooleanField(default=True)

    def __str__(self):
        return "%s-%s" % (self.hostname, self.ip_addr)


class HostGroup(models.Model):
    """
    host group
    """
    name = models.CharField(max_length=64, unique=True)
    host_user_binds = models.ManyToManyField("HostUserBind")

    def __str__(self):
        return self.name


class HostUser(models.Model):
    """
    all host login user info
    """
    auth_type_choice = ((0, 'ssh-password'), (1, 'ssh-key'))
    auth_type = models.SmallIntegerField(choices=auth_type_choice)
    username = models.CharField(max_length=32)
    password = models.CharField(max_length=64, blank=True, null=True)

    def __str__(self):
        return "%s-%s-%s" % (
            self.get_auth_type_display(), 
            self.username,
            self.password
        )
    
    class Meta:
        unique_together = ('username', 'password')


class HostUserBind(models.Model):
    """
    bind host and login user
    """
    host = models.ForeignKey('Host')
    host_user = models.ForeignKey('HostUser')

    def __str__(self):
        return "%s-%s" % (self.host, self.host_user)

    class Meta:
        unique_together = ('host', 'host_user')


class AuditLog(models.Model):
    """
    log table
    """


class Account(models.Model):
    """
    web login account
    """
    user = models.OneToOneField(User)
    name = models.CharField(max_length=64)
    host_user_binds = models.ManyToManyField('HostUserBind', blank=True)
    host_groups = models.ManyToManyField('HostGroup', blank=True)
