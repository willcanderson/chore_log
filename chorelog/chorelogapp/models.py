from django.db import models
from django.contrib.auth.models import AbstractUser

class User(AbstractUser):
    USER_TYPE_CHOICES = (
        ('PARENT', 'Parent'),
        ('CHILD', 'Child'),
    )
    user_type = models.CharField(max_length=6, choices=USER_TYPE_CHOICES)

class Parent(models.Model):
    """
    Extends the base User model
    """
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='parent_profile')

    def __str__(self):
        return f"Parent: {self.user.get_full_name()}"
    
class Child(models.Model):
    """
    Extends base User model and references a parent
    """
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='child_profile')
    parent = models.ForeignKey(Parent, on_delete=models.CASCADE, related_name='children')

    def __str__(self):
        return f"Child: {self.user.get_full_name()} (Parent: {self.parent.user.get_full_name()})"