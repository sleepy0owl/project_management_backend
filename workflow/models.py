from typing import Tuple
from django import db
from django.db import models
from user_management.models import Users

# Create your models here.
class WorkflowBoard(models.Model):
    board_id = models.AutoField(primary_key=True)
    board_name = models.CharField(max_length=100, null=False)
    board_description = models.CharField(max_length=254)
    updated_on = models.DateTimeField(null=False, auto_now=True)
    user = models.ForeignKey(Users, on_delete=models.CASCADE, related_name='board')

    class Meta:
        db_table = 'project_board'

class BoardList(models.Model):
    list_id = models.AutoField(primary_key=True)
    list_name = models.CharField(max_length=45, null=False)
    updated_on = models.DateTimeField(null=False, auto_now=True)
    board = models.ForeignKey(WorkflowBoard, on_delete=models.CASCADE, related_name='list')

    class Meta:
        db_table = 'project_board_list'

class Card(models.Model):
    card_id = models.AutoField(primary_key=True)
    card_name = models.CharField(max_length=100, null=False)
    card_desciption = models.CharField(max_length=254)
    updated_on = models.DateTimeField(null=False, auto_now=True)
    board_list = models.ForeignKey(BoardList, on_delete=models.CASCADE, related_name='card')

    class Meta:
        db_table = 'project_list_card'
