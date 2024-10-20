from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
from datetime import timedelta
from django.utils.crypto import get_random_string

class UserToken(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='token')
    token = models.CharField(max_length=64, unique=True)
    token_created_at = models.DateTimeField(auto_now_add=True)

    def is_token_expired(self):
        # Check if the token is older than 1 day
        expiration_time = self.token_created_at + timedelta(days=1)
        return timezone.now() > expiration_time

    def regenerate_token(self):
        # Regenerate token and reset timestamp
        self.token = get_random_string(length=64)  # Generate a new token
        self.token_created_at = timezone.now()
        self.save()



class Team(models.Model):
    name = models.CharField(max_length=100,unique=True)
    leader = models.OneToOneField(User, on_delete=models.CASCADE, related_name='teams')
    leader_contact = models.CharField(max_length=12)
    member1_name = models.CharField(max_length=100)
    member2_name = models.CharField(max_length=100)
    member3_name = models.CharField(max_length=100)
    # problem_solution_file = models.FileField(upload_to='static/problem_solutions/')

    def __str__(self):
        return self.name
    
class ProblemSubmission(models.Model):
    team = models.ForeignKey(Team, on_delete=models.CASCADE)
    problem_solution_file = models.FileField(upload_to='static/problem_solutions/')
    submission_time = models.DateTimeField(auto_now_add=True)
    title = models.CharField(max_length=100)
    description = models.TextField()
    status_choice = [
        ('Pending', 'Pending'),
        ('Accepted', 'Accepted'),
        ('Rejected', 'Rejected'),
    ]
    status = models.CharField(max_length=10, choices=status_choice, default='Pending')

    def __str__(self):
        return self.team.name
    
class submissiontime(models.Model):
    tag = models.CharField(max_length=100,primary_key=True)
    submission_time = models.DateTimeField()
    def __str__(self):
        return str(self.submission_time)
    

class contact(models.Model):
    email = models.EmailField()
    message = models.TextField()
    action_choice = [
        ('Pending', 'Pending'),
        ('Accepted', 'Accepted'),
    ]
    action = models.CharField(max_length=10, choices=action_choice, default='Pending')
    def __str__(self):
        return self.message
    

