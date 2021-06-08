from django.db import models
from django.db.models.base import Model

# Create your models here.
class Users(models.Model):
    user_id = models.AutoField(primary_key=True)
    first_name = models.CharField(max_length=45, null=False)
    last_name = models.CharField(max_length=45, null=False)
    username = models.CharField(max_length=45, null=False)
    email_address = models.EmailField(max_length=254, null=False)
    password = models.CharField(max_length=100, null=False)
    subscription_type = models.IntegerField(null=False) 
    created_on = models.DateTimeField(null=False, auto_now=True)
    class Meta:
        db_table = 'project_users'