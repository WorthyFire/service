from django.contrib.auth.models import User
from django.db import models

class CustomUser(User):
    full_name = models.CharField(max_length=255)
    consent_to_process_data = models.BooleanField(default=False)
