from django.db import models
from django.contrib.gis.db import models as gis_models
import logging
from django.contrib.auth.models import User, update_last_login
from django.conf import settings
from django.utils import timezone
from phonenumber_field.modelfields import PhoneNumberField
from django.core.validators import RegexValidator

class Constituency(models.Model):
    objectid = models.FloatField()
    const_nam = models.CharField(max_length=50)
    const_no = models.FloatField()
    county_nam = models.CharField(max_length=50)
    st_area_sh = models.FloatField()
    st_length_field = models.FloatField()
    shape_leng = models.FloatField()
    shape_area = models.FloatField()
    globalid = models.CharField(max_length=254)
    geom = gis_models.MultiPolygonField(srid=4326)

    class Meta:
        verbose_name_plural = 'Constituencies'

    def __str__(self):
        return 'Constituency Name'.format(self.const_nam)    

class Companies(models.Model):
    company_na = models.CharField(max_length=254)
    address = models.CharField(max_length=254)
    lat = models.FloatField()
    long = models.FloatField()
    geom = gis_models.PointField(srid=4326)




stakeholder_type = (
    ('Exporters','Exporters'),
    ('Supplier','Suppliers'),
    ('Company','Company'),
    ('Broker','Broker'),
)

phone_regex = RegexValidator(regex=r'^\+?1?\d{13,15}$',message='phone number is in the format 0703111222, up to 10 digits allowed')
category = (
    ('Pests','Pests'),
    ('Diseases','Diseases'),
    ('Natural occurences','Natural occurences'),
    ('Corning','Corning'),
    ('Other','Other'),
)

incidence_status = (
    ('Closed','Closed'),
    ('Still Open','Still Open'),
    ('UnSolved','UnSolved'),
)


class Stakeholders(models.Model):
    id = models.AutoField(primary_key=True,null=False)
    name = models.CharField(max_length=50,null=False)
    email = models.EmailField(max_length=100,null=False)
    telephone = models.CharField(max_length=15)
    dealer = models.CharField(max_length=50,choices=stakeholder_type)
    physical_address = models.CharField(max_length=100, null=False)

class Fertilizers(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=100,null=False)
    weight = models.CharField(max_length=10)
    description = models.TextField(max_length=200)
    price = models.CharField(max_length=100)

    
class HarvestDetails(models.Model):
    id = models.AutoField(primary_key=True)
    date = models.DateField(null=False)
    fruits = models.IntegerField(null=False)
    weight = models.CharField(max_length=10,null=True)


class Seedlings(models.Model):
    id = models.AutoField(primary_key=True)
    cultivar = models.CharField(max_length=20,null=False)
    description = models.TextField(max_length=200)
    price = models.CharField(max_length=20)
    image = models.ImageField(upload_to='cultivars',null=False)

class PruningCare(models.Model):
    method = models.CharField(max_length=50,null=False)
    description = models.TextField(max_length=200)


class Incidences(models.Model):
    incidence_id = models.AutoField(primary_key=True)
    user = models.ForeignKey(User,on_delete=models.CASCADE,default=1)
    email = models.EmailField(max_length=100, null=False)
    phonenumber = models.CharField(max_length=15)
    incidence_date = models.DateTimeField(auto_now_add=True, null=False)
    incidence_type = models.CharField(max_length=50, choices=category)
    incidence_description = models.TextField(max_length=200)
    nearest_town = models.CharField(max_length=50,null=True)
    status= models.CharField(max_length=20,choices=incidence_status)
    location = gis_models.PointField(srid=4326)

    class Meta:
        verbose_name_plural = 'Reported Incidences'

class PickupSchedules(models.Model):
    route_name = models.CharField(verbose_name='Route Name', max_length=100)
    stakeholder = models.CharField(max_length=30,choices=stakeholder_type,null=False)
    departure = models.DateTimeField(verbose_name='Departure')
    stops = models.CharField(max_length=300, verbose_name='Stop Locations')
    source = models.CharField(max_length=30,null=False)


class StaffProfiles(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    telnumber = models.CharField(max_length=10,verbose_name='Phone Number')
    address = models.CharField(max_length=200,verbose_name='Address')
    photo = models.ImageField(verbose_name='Profile Picture')

    def __str__(self):
        return 'User is {}'.format(self.user.username)

