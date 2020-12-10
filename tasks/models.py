from users.models import UserToken
from django.db import models
from django.utils import timezone

# Create your models here.
class Task(models.Model):
    id = models.UUIDField(max_length=120, unique=True, primary_key=True)
    author_token = models.ForeignKey(UserToken, on_delete=models.CASCADE)
    task = models.CharField(max_length=1500)
    status = models.BooleanField()
    priority = models.CharField(max_length=30)
    initial_date = models.DateField()
    limit_date = models.DateField()
    accomplishment_date = models.DateField(default=timezone.now())
