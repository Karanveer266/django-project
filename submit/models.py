from django.db import models
from problems.models import Problem # Import the Problem model


class Submission(models.Model):
    problem = models.ForeignKey(Problem, on_delete=models.CASCADE)
    code = models.TextField()
    language = models.CharField(max_length=50)
    input_data = models.TextField(blank=True, null=True)
    output_data = models.TextField(blank=True, null=True)
    error_data = models.TextField(blank=True, null=True)
    status = models.CharField(max_length=50, default='PENDING')
    submitted_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Submission for {self.problem.title} - {self.status}"
