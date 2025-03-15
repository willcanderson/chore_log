from django.db import models
from django.contrib.auth.models import AbstractUser

class User(AbstractUser):
    USER_TYPE_CHOICES = (
        ('PARENT', 'Parent'),
        ('CHILD', 'Child'),
    )
    user_type = models.CharField(max_length=6, choices=USER_TYPE_CHOICES)
    parent = models.ForeignKey('self', on_delete=models.CASCADE, related_name='children', null=True, blank=True)
    
class Chore_Definition(models.Model):
    name = models.CharField(max_length=50)
    minute_value = models.IntegerField()
    defined_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name='defined_chores')

    def __str__(self):
        return f"Chore: {self.name}, worth {self.minute_value} minutes"

class Work(models.Model):
    chore = models.ForeignKey(Chore_Definition, on_delete=models.SET_NULL, null=True)
    done_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name='work_done')
    date_logged = models.DateField(auto_now_add=True)

    def __str__(self):
        return f"Chore: {self.chore.name} logged by {self.done_by} on {self.date_logged}"

class Play(models.Model):
    game = models.CharField(max_length=50)
    minutes_played = models.IntegerField()
    child = models.ForeignKey(User, on_delete=models.CASCADE, related_name='play_done')
    date_logged = models.DateField(auto_now_add=True)

    def __str__(self):
        return f"{self.game} played by {self.child} for {self.minutes_played} minutes on {self.date_logged}"
