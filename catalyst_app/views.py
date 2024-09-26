from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login, logout
from django.contrib import messages 
from .models import CSVFile, Company
import csv 
import threading


# Create your views here.

def register(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            print("done registration")
            return redirect('myapp:login')
        else:
            print("there is something wrong")
            print(form.errors)
    else:
        form = UserCreationForm()
    return render(request, 'catalyst_app/register.html',{'form':form})


def login_view(request):
    if request.method == "POST":
        form =  AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            #url name
            return redirect('myapp:home')
    else:
        form = AuthenticationForm()

    return render(request, "catalyst_app/login.html", {'form':form})

# def logout_view(request):
#     logout(request)
#     return redirect('login')

def process_csv(file_path):
    with open(file_path, newline='') as f:
        reader = csv.reader(f)
        for row in reader:
            #process each row (save to the db)
            pass

@login_required
def homePage(request):
    if request.method == 'POST':
        csv_file = request.FILES.get('file')  #retrieve the uploaded file from the post request
        if csv_file and csv_file.name.endswith('.csv'):
            #save the file
            saved_file = CSVFile.objects.create(file=csv_file)
            messages.success(request, 'File uploadedsuccessfully!')
            
            #process the file in the background
            threading.Thread(target=process_csv, args=(saved_file.file.path,)).start()

            return redirect('myapp:home')
        else:
            messages.error(request, 'Please upload a valid CSV file')

        
     
    return render(request,'catalyst_app/home.html')


@login_required
def query_builder(request):
    keyword = request.GET.get('keyword','')
    industry = request.GET.get('industry','')
    year_founded = request.GET.get('year_founded','')
    city = request.GET.get('city','')
    state = request.GET.get('state','')
    country = request.GET.get('country','')
    employees_from = request.GET.get('employees_from','')
    employees_to = request.GET.get('employees_to','')

    companies = Company.objects.all()

    #apply fileters
    if keyword:
        companies = companies.filter(name__icontains=keyword)
    if industry:
        companies = companies.filter(industry=industry)
    if year_founded:
        companies = companies.filter(year_founded=year_founded)
    if city:
        companies = companies.filter(city=city)
    if state:
        companies = companies.filter(state=state)
    if country:
        companies =companies.filter(country=country)
    if employees_from:
        companies = companies.filter(employees__gte=employees_from)
    if employees_to:
        companies = companies.filter(employees__lte=employees_to)

    #count the filtered records
    company_count = companies.count()

    context = {
        'companies':companies,
        'company_count':company_count,
    }

    return render(request,'catalyst_app/query-builder.html', context)


@login_required
def users_detail(request):
    user_data = request.user
    print(user_data)
    return render(request,'catalyst_app/users-detail.html',{'user_data':user_data})




