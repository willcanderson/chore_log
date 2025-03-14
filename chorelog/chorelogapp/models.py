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
    
class Chore_Definition(models.Model):
    name = models.CharField(max_length=50)
    minute_value = models.IntegerField()
    defined_by = models.ForeignKey(Parent, on_delete=models.CASCADE, related_name='defined_chores')

    def __str__(self):
        return f"Chore: {self.name}, worth {self.minute_value} minutes"

class Work(models.Model):
    chore = models.ForeignKey(Chore_Definition, on_delete=models.SET_NULL, null=True)
    done_by = models.ForeignKey(Child, on_delete=models.CASCADE, related_name='work_done')
    date_logged = models.DateField.auto_now_add()

    def __str__(self):
        return f"Chore: {self.chore.name} logged on {self.date_logged}"

class Play(models.Model):
    game = models.CharField(max_length=50)
    minutes_played = models.IntegerField()
    child = models.ForeignKey(Child, on_delete=models.CASCADE, related_name='play_done')
    date_logged = models.DateField.auto_now_add()

    def __str__(self):
        return f"Chore: {self.game} logged on {self.date_logged}"
