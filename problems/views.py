from django.shortcuts import render
from django.http import HttpResponse 
from .models import Problem

def problem_list(request):
    problems = Problem.objects.all()
    return render(request, 'problems/problem_list.html', {'problems': problems})

def problem_detail(request, pk):
    problem = Problem.objects.get(pk=pk)
    return render(request, 'problems/problem_detail.html', {'problem': problem})

def problem_create(request):
    # This is a placeholder. You'll need to implement the actual logic for creating a problem here.
    # For now, it can just redirect to the problem list or render a form.
    return HttpResponse("Problem creation page (placeholder)")

# Create your views here.
