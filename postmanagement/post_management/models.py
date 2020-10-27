from django.db import models
from accounts.models import User

POST_TYPE=(('1', 'COD'),('2','PAID'))
PRIORITY = (('1', 'high'),('2','medium'),('3','low'),('4','normal'))
STATUS=(('1','assigned'),('2','completed'),('3','rejected'))
# Create your models here.


class TaskWork(models.Model):
    id=models.CharField(unique=True,primary_key=True,auto_created=True,max_length=20)
    assigned_to = models.ForeignKey(User, on_delete=models.CASCADE,related_name="task")
    source = models.CharField(max_length=10)
    post_type = models.CharField(max_length=10,choices=POST_TYPE)
    priority = models.CharField(max_length=10, choices=PRIORITY)
    remarks = models.TextField()
    task_status = models.CharField(max_length=10,choices=STATUS)

    def __str__(self):
        return self.id


class Customer(models.Model):
    name=models.CharField(max_length=30)
    mobile=models.CharField(max_length=20)
    address=models.TextField()

    def __str__(self):
        return self.name