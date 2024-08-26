from django.db import models

# Create your models here.
class JobPosting(models.Model):  
    # id - starts at 1 and autoincrements
    title = models.CharField(max_length=100) # mysql varchar(100)
    description = models.TextField() # mysql text
    company = models.CharField(max_length=100)
    salary = models.IntegerField() # mysql int
    is_active=models.BooleanField(default=False)

    def __str__(self):
        return f"{self.title} | {self.company} | Active: {self.is_active}"