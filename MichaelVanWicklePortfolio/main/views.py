from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse, Http404
from django.template import loader

from .models import Job, Award

# Create your views here.

def index(request):
    job_list = Job.objects.order_by('-start_date')
    award_list = Award.objects.order_by('-date_awarded')
    context = {'job_list': job_list, 'award_list': award_list}
    return render(request, 'main/index.html', context)

def jobs(request):
    job_list = Job.objects.order_by('-start_date')
    context = {'job_list': job_list}
    return render(request, 'main/jobs.html', context)

def awards(request):
    award_list = Award.objects.order_by('-date_awarded')
    context = {'award_list': award_list}
    return render(request, 'main/awards.html', context)

def job_detail(request, job_id):
    job = get_object_or_404(Job, pk=job_id)
    return render(request, 'main/detail.html', {'job': job})

def award_detail(request, award_id):
    award = get_object_or_404(Award, pk=award_id)
    return render(request, 'main/detail.html', {'award': award})