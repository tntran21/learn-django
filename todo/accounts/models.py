from django.db import models
from django.contrib.auth.hashers import make_password, check_password


# Create your models here.
class Accounts(models.Model):
    user_name = models.CharField(max_length=50)
    email = models.EmailField()
    password = models.CharField(max_length=50)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return self.email

    def set_password(self, password):
        self.password = make_password(password)

    def check_password(self, password):
        return check_password(password, self.password)

    def set_created_at(self, now=False):
        self.created_at = now
        return self.created_at
