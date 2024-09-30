from django.db import models

# Create your models here.
class CSVFile(models.Model):
    file = models.FileField(upload_to = 'uploads/')
    uploaded_at =models. DateTimeField(auto_now_add = True)

    def __str__(self):
        return self.file.name

class CompanyInfo(models.Model):
    name = models.CharField(max_length=100)
    industry = models.CharField(max_length=100)
    year_founded = models.IntegerField()
    city = models.CharField(max_length=100)
    state = models.CharField(max_length=100)
    country = models.CharField(max_length=100)
    employees = models.IntegerField()

    def __str__(self):
        return self.name