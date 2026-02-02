from django.db import models
from accounts.models import User, BaseModel

LOW = 0
MEDIUM = 1
HIGH = 2

PRIORITY_CHOICES = [
    (LOW, 'Low'),
    (MEDIUM, 'Medium'),
    (HIGH, 'High'),
]

TODO = 0
IN_PROGRESS = 1
DONE = 2

STATUS_CHOICES = [
    (TODO, 'To Do'),
    (IN_PROGRESS, 'In Progress'),
    (DONE, 'Done'),
]


class Issue(BaseModel):
    title = models.CharField(max_length=255)
    description = models.TextField(blank=True)
    status = models.IntegerField(
        choices=STATUS_CHOICES,
        default=TODO
    )
    priority = models.IntegerField(
        choices=PRIORITY_CHOICES,
        default=MEDIUM
    )
    assigned_to = models.ForeignKey(User, on_delete=models.CASCADE, related_name='issues')

    def __str__(self):
        return self.title