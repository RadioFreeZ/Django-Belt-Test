from django.shortcuts import render, HttpResponse, redirect
import bcrypt
from django.contrib import messages
from .models import User,Job
import datetime
from datetime import timedelta
def dash(request):
    return render(request,'dash.html')

def register(request):
    if request.method == 'POST':
        context = {
            'first_name' : request.POST['first_name'],
            'last_name' : request.POST['last_name'],
            'email' : request.POST['email'],
            'password' : request.POST['password'],
            'password_confirm' : request.POST['password_confirm'],
            'birthday' : request.POST['birthday'],
        }

        errors = User.objects.basic_validator(request.POST)
        if not context['birthday']:
            errors["birthday"] = "Invalid Birthday"
        if context['password'] != context['password_confirm']:
            errors["password"] = "Passwords must match!"
        if len(errors):
            for key, value in errors.items():
                messages.error(request, value)
            return redirect('/')
        hash = bcrypt.hashpw(context['password'].encode(), bcrypt.gensalt())
        User.objects.create(first_name = context['first_name'], last_name = context['last_name'], email = context['email'], password = hash, birthday = context['birthday'])
        request.session['user_id']=User.objects.last().id
        request.session['name']=context['first_name']
        return redirect('/dashboard')
    else:
        return redirect('/')

def login(request):
    context = {
        'email' : request.POST['email'],
        'password' : request.POST['password']
    }
    check = User.objects.filter(email = context['email'])
    if check:
        user = User.objects.get(email = context['email'])
        if user.email:
            if bcrypt.checkpw(context['password'].encode(), user.password.encode()):
                request.session['user_id']=user.id
                request.session['name']=user.first_name
                return redirect('/dashboard')
    errors = {}
    errors['login'] = "Login incorrect!"
    for key, value in errors.items():
        messages.error(request, value)
        return redirect('/')
def logout(request):
    request.session.clear()
    return redirect('/')

def dashboard(request):
    context = {}
    context['jobs'] = Job.objects.all()
    return render(request, 'dashboard.html', context)

def edit(request, id):
    context = {}
    context['job_id'] = id
    context['jobs'] = Job.objects.get(id=id)
    return render(request,"edit.html",context)

def update(request, id):
    context = {
        'title' : request.POST['title'],
        'description' : request.POST['description'],
        'location' : request.POST['location'],
    }
    errors = Job.objects.job_validator(request.POST)
    if len(errors):
        for key, value in errors.items():
            messages.error(request, value)
        return redirect('/jobs/edit/'+str(id))
    job = Job.objects.get(id=id)
    job.title = context['title']
    job.description = context['description']
    job.location = context['location']
    job.save()
    return redirect('/dashboard')

def new(request):
    return render(request, 'new.html')

def create(request):
    context = {
        'title' : request.POST['title'],
        'description' : request.POST['description'],
        'location' : request.POST['location'],
        'cat2' : request.POST['cat2']
    }
    try:
        context['cat1'] = request.POST['cat1']
    except:
        context['cat1'] = ""
    errors = Job.objects.job_validator(request.POST)
    if len(errors):
        for key, value in errors.items():
            messages.error(request, value)
        return redirect('/jobs/new/')
    if len(context['cat1']) < 1:
        category = context['cat2']
    elif len(context['cat2']) < 1:
        category = context['cat1']
    else:
        category = f"{context['cat1']}, {context['cat2']}"
    Job.objects.create(title = context['title'], description = context['description'], location = context['location'], category = category, poster_id = request.session['user_id'], worker_id = 0)
    return redirect('/dashboard')

def view(request,id):
    context = {}
    context['job'] = Job.objects.get(id = id)
    context['user'] = User.objects.get(id=context['job'].poster_id)
    return render(request,'view.html',context)

def add(request,id):
    job = Job.objects.get(id = id)
    job.worker_id = request.session['user_id']
    job.save()
    return redirect('/dashboard')

def delete(request, id):
    job = Job.objects.get(id = id)
    job.delete()
    return redirect('/dashboard')
def give(request, id):
    job = Job.objects.get(id = id)
    job.worker_id = 0
    job.save()
    return redirect('/dashboard')
