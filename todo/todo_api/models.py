from django.db import models


class User(models.Model):
    id = models.AutoField(primary_key=True)
    user_name = models.CharField(max_length=120)
    email = models.EmailField(max_length=120)
    password = models.CharField(max_length=120)

    def __str__(self):
        return self.username


# Create your models here.
class Todo(models.Model):
    id = models.AutoField(primary_key=True)
    user_id = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=120)
    description = models.TextField()
    completed = models.BooleanField(default=False)

    def __str__(self):
        return self.title
