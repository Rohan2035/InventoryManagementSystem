from email.policy import default
from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class profile(models.Model):

    staff = models.OneToOneField(User, on_delete=models.CASCADE, null=True)
    address = models.CharField(max_length=200, null=True)
    phone = models.CharField(max_length=10, null=True)
    image = models.ImageField(default='p_default.jpg', upload_to='Profile_Images')
    user_message = models.CharField(max_length=300, null=True)

    def __str__(self) -> str:
        return f'{self.staff.username}-Profile'



