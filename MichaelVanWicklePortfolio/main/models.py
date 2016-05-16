from django.db import models

# Create your models here.


class Job(models.Model):
    job_title = models.CharField(verbose_name='Job Title', max_length=200)
    company_name = models.CharField(verbose_name='Company Name', max_length=200)
    start_date = models.DateField(verbose_name='Start Date')
    end_date = models.DateField(verbose_name='End Date')
    def __str__(self):
        return ' at '.join([self.job_title, self.company_name])


class VolunteerPos(models.Model):
    title = models.CharField(verbose_name='Title', max_length=200)
    site = models.CharField(verbose_name='Location', max_length=200)
    organization = models.CharField(max_length=200)
    num_hours = models.IntegerField(verbose_name='Hours Worked')
    start_date = models.DateField(verbose_name='Start Date')
    end_date = models.DateField(verbose_name='End Date')
    class Meta:
        verbose_name = 'Volunteer Position'
        verbose_name_plural = 'Volunteer Positions'
    def __str__(self):
        return ' at '.join([self.title, self.site])
    

class Activity(models.Model):
    name_of_group = models.CharField(max_length=200)
    position_held = models.CharField(verbose_name='Position Held', blank=True, max_length=200)
    start_date = models.DateField(verbose_name='Start Date')
    end_date = models.DateField(verbose_name='End Date')
    class Meta:
        verbose_name_plural = 'Activities'
    def __str__(self):
        return self.name_of_group 


class Award(models.Model):
    name = models.CharField(verbose_name='Name of Award', max_length=200)
    reason = models.TextField(verbose_name='Reason for Award')
    date_awarded = models.DateField(verbose_name='Date Awarded')
    def __str__(self):
        return self.name
