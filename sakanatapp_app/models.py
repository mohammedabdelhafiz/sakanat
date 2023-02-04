from django.db import models

# Create your models here.
from django.db import models
import bcrypt
import re

NAME_REGEX = re.compile(r'[a-zA-Z]+$')
EMAIL_REGEX = re.compile(r'[a-zA-Z0-9.+_-]+@[a-zA_Z0-9._-]+\.[a-zA-z]+$')

# UserManager class is used to handle the validation for user registration and login
class UserManager(models.Manager):
    def validate_register(self, postData):
        errors = {}
        if len(postData['name']) < 2:
            errors['Name'] = "Name should be at least 2 characters"
        elif not NAME_REGEX.match(postData['name']):
            errors['Name'] = "Name should contain letters only"
        if not EMAIL_REGEX.match(postData['email']):
            errors['email'] = "Invalid email format"
        elif len(User.objects.filter(email = postData['email'])) > 0:
            errors['email'] = "Email already registered"
        if len(postData['pass']) < 8:
            errors['password'] = "Password should be at least 8 characters"
        if postData['pass'] != postData['cpass']:
            errors['password_confirm'] = "Passwords do not match"
        if len(postData['phone']) < 2:
            errors['Phone'] = "Phone Number  should be at least 10 numbers "
        return errors

    def login_validator(self,postData):
        errors={}
        my_user=User.objects.filter(email=postData['email'])
        if len(my_user)==0:
            errors['email']=f"this email {postData['email']} have no account, please enter correct email or go to sign up to create a new user"
        else:
            real_password=my_user[0].password
            if  not bcrypt.checkpw(postData['password'].encode(), real_password.encode()):
                errors['password']="incorrect password please try again"
        return errors


class User(models.Model):

        name = models.CharField(max_length=25)
        email = models.CharField(max_length=255)
        location = models.CharField(max_length=50)
        city = models.CharField(max_length=50)
        phone_number = models.IntegerField()
        password = models.CharField(max_length=100)
        created_at = models.DateTimeField(auto_now_add=True)
        updated_at = models.DateTimeField(auto_now=True)
        objects = UserManager()
        # apartments 
        # chalets

class Apartment(models.Model):
    location = models.CharField(max_length=50)
    city = models.CharField(max_length=50)
    area= models.CharField(max_length=100)
    user = models.ForeignKey(User , on_delete=models.CASCADE , related_name="apartments")
    cost = models.IntegerField()
    hall = models.CharField(max_length=3)
    kitchen = models.CharField(max_length=3)
    balcony = models.CharField(max_length=3)
    bedrooms = models.IntegerField()
    AC = models.CharField(max_length=3)
    img = models.ImageField(upload_to='files/apartments/', height_field=None, width_field=None, max_length=100)
    desc = models.CharField(max_length=200)
    # messages 

class Chalet(models.Model):
    location = models.CharField(max_length=50)
    city = models.CharField(max_length=50)
    area= models.CharField(max_length=100)
    user = models.ForeignKey(User , on_delete=models.CASCADE , related_name="chalets")
    cost = models.IntegerField()
    hall = models.CharField(max_length=3)
    kitchen = models.CharField(max_length=3)
    balcony = models.CharField(max_length=3)
    bedrooms = models.IntegerField()
    AC = models.CharField(max_length=3)
    pool = models.CharField(max_length=3)
    desc = models.CharField(max_length=200)
    img = models.ImageField(upload_to='files/chalet/', height_field=None, width_field=None, max_length=100)
    # messages 

class Message(models.Model):
    name = models.CharField(max_length=255)
    email = models.EmailField()
    subject = models.CharField(max_length=255)
    message = models.TextField()
    apartment = models.ForeignKey(Apartment ,on_delete=models.CASCADE , related_name='messages')
    chalet = models.ForeignKey(Chalet,on_delete=models.CASCADE , related_name='messages')
    created_at = models.DateTimeField(auto_now_add=True)














def create_user(name ,email , location , city , phone_number, password):
    return User.objects.create(name=name , email=email, location=location , city=city, phone_number=phone_number, password=password)

def create_apartment(location , city  , area , user ,  cost , hall , kitchen , balcony , bedrooms ,AC , desc , img ):
    return Apartment.objects.create(location=location , city= city  ,area=area ,user=user, cost=cost , hall=hall , kitchen=kitchen , balcony=balcony , bedrooms=bedrooms,AC=AC , desc=desc , img = img )


def create_chalet(location , city  , area , user ,  cost , hall , kitchen , balcony , bedrooms ,AC, pool , desc , img ):
    return Chalet.objects.create(location=location , city= city  ,area=area ,user=user, cost=cost , hall=hall , kitchen=kitchen , balcony=balcony , bedrooms=bedrooms,AC=AC,pool=pool , desc=desc , img = img )





def get_users_list(email):
    return User.objects.filter(email=email)

def get_user_id(id):
    user =  User.objects.get(id=id)
    return user

def logged_user(email):
    my_users=User.objects.filter(email=email)
    my_user=my_users[0]
    return my_user.id


def update(location , city  , area , user ,  cost , hall , kitchen , balcony , bedrooms ,AC , desc , apartment_id ):
    my_apartment=Apartment.objects.get(id=apartment_id)
    my_apartment.location=location
    my_apartment.city=city
    my_apartment.area=area
    my_apartment.user=user
    my_apartment.cost=cost
    my_apartment.hall=hall
    my_apartment.kitchen=kitchen
    my_apartment.balcony=balcony
    my_apartment.bedrooms=bedrooms
    my_apartment.AC=AC
    my_apartment.desc=desc
    my_apartment.save()

def delete_apartment(apartment_id):
    apartment = Apartment.objects.get(id=apartment_id)
    apartment.delete()










