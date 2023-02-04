from django.shortcuts import render, HttpResponse , redirect
from .models import User
from django.contrib import messages
import bcrypt
from . import models
from .models import * 




def index(request):
    context = {}

    apartment = Apartment.objects.all()
    
    if bool(apartment):
        n = len(apartment)
        nslide = n // 3 + (n % 3 > 0)
        apartments = [apartment, range(1, nslide), n]
        context.update({'apartments': apartments})
    #context = {
        #'apartments' : Apartment.objects.all()
    #}
    chalet = Chalet.objects.all()
    if bool(chalet):
        n = len(chalet)
        nslide = n // 3 + (n % 3 > 0)
        chalets = [chalet, range(1, nslide), n]
        context.update({'chalet': chalets})
    return render (request , 'index.html' , context)

def register_user(request):
    errors = User.objects.validate_register(request.POST)
    if request.method == 'POST':
        if len(errors) >0 :
            for key, value in errors.items():
                messages.error(request ,value)
            context = {'name' : request.POST['name'] ,'email' : request.POST['email'] , 'location' : request.POST['location'] , 'city' : request.POST['city'] , 'phone' : request.POST['phone']  }
            return render (request , 'register.html' , context)
            #return redirect('/register_page') 
        else:
            user = request.POST
            password =user['pass']
            PW_hash = bcrypt.hashpw(password.encode(),bcrypt.gensalt()).decode()
            create_user(user['name'] ,user['email'] , user['location'] , user['city'] ,user['phone']   , PW_hash )
            return redirect('/') 

def login_user(request):
    errors = User.objects.login_validator(request.POST)
    if request.method == 'POST':
        if len(errors) >0 :
            for key, value in errors.items():
                messages.error(request ,value)
            return redirect('/login_page')
        else:
            email=request.POST['email']
            logged_user_id=logged_user(email)
            request.session['current_user_id']=logged_user_id
            return redirect('/success')

def success_login(request ):
    if 'current_user_id' not in request.session:
        messages.error(request ,'You must login to view that page')
        return redirect('/')
    else:

        context = {
            "user": get_user_id(request.session['current_user_id']),
            "added_apartments_no":User.objects.get(id=request.session["current_user_id"]).apartments.all().count(),
            "added_chalets_no" : User.objects.get(id=request.session["current_user_id"]).chalets.all().count(),

        }
        return render(request ,'profile.html', context )

def register_page(request):
        return render(request, 'register.html')

def login_page(request): 
    return render(request, 'login.html')

def search_page(request): 

    return render(request, 'Search.html')

def edit_page(request , apartment_id):

    context = {
        'apartment' : Apartment.objects.get(id=apartment_id)
    }

    return render(request, 'edit.html' , context)

def about_page(request): 
    return render(request, 'about.html')

def contact_page(request): 
    return render(request, 'contact.html')

def logout_user(request):
    request.session.clear()
    return redirect("/")


def apartment_form(request):
    return render(request, 'post.html')

def add_apartment(request):
    
    apartment = request.POST
    user = get_user_id(request.session['current_user_id'])
    create_apartment(apartment['location'] , apartment['city'] , apartment['area'] , user , apartment['cost'] , apartment['hall'] , apartment['kitchen'] , apartment['balcony'] , apartment['bedroom'] ,apartment['AC']  , apartment['desc'] ,request.FILES['img'] )
    return redirect('/') 

def search(request):
    context = {}
    if request.method == 'GET':
        typ = request.GET['type']
        q = request.GET['q']
        context.update({'type': typ})
        context.update({'q':q})
        results={}
        if typ == 'Chalet' and (bool(Chalet.objects.filter(location=q)) or bool(Chalet.objects.filter(city=q))):
            results = Chalet.objects.filter(location=q)
            results = results | Chalet.objects.filter(city=q)
        elif typ == 'Apartment'  and (bool(Apartment.objects.filter(location=q)) or bool(Apartment.objects.filter(city=q))):
            results = Apartment.objects.filter(location=q)
            results = results | Apartment.objects.filter(city=q)

        
        if bool(results)== False:
            print("messages")
            messages.success(request, "No matching results for your query..")

        result = [results, len(results)]
        context.update({'result': result})

    return render(request, 'Search.html' , context)

def Apartment_detail(request, apartment_id): 

    #apartment =  Apartment.objects.get(id=apartment_id)
    context = {
        'apartment': Apartment.objects.get(id=apartment_id),
        #"user": get_user_id(request.session['current_user_id']),

    }
    return render(request, 'desc.html', context)

def delete(request , apartment_id):
    delete_apartment(apartment_id)
    return redirect('/success')

def update_apartment(request):
    apartment = request.POST
    user = get_user_id(apartment['user_id'])

    update(apartment['location'] , apartment['city'] , apartment['area'] , user , apartment['cost'] , apartment['hall'] , apartment['kitchen'] , apartment['balcony'] , apartment['bedroom'] ,apartment['AC']  , apartment['desc'] , apartment['id'])

    return redirect(f'/{apartment["id"]}')

def chalet_form(request):
    return render(request, 'posth.html')

def add_chalet(request):
    chalet = request.POST
    user = get_user_id(request.session['current_user_id'])
    create_chalet(chalet['location'] , chalet['city'] , chalet['area'] , user , chalet['cost'] , chalet['hall'] , chalet['kitchen'] , chalet['balcony'] , chalet['bedroom'] ,chalet['AC'] , chalet['pool']  , chalet['desc'] ,request.FILES['img'] )
    return redirect('/') 

def chalet_detail(request, chalet_id): 

    #apartment =  Apartment.objects.get(id=apartment_id)
        context = {
        'chalet': Chalet.objects.get(id=chalet_id),
        #"user": get_user_id(request.session['current_user_id']),

    }
        return render(request, 'desc_h.html', context)