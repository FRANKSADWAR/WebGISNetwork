from django import forms
from django.forms import ValidationError, widgets
from django.contrib.gis import forms as gis_forms
from django.contrib.auth.models import User
from flatpickr import DatePickerInput, TimePickerInput, DateTimePickerInput
from geoapp.models import HarvestDetails, Incidences, PickupSchedules, StaffProfiles
from leaflet.forms.widgets import LeafletWidget
from mapwidgets.widgets import GooglePointFieldWidget, GoogleStaticMapWidget, GoogleStaticOverlayMapWidget




import logging

logger = logging.getLogger(__name__)

# The user login form into the site    
class LoginForm(forms.Form):
    username = forms.CharField()
    password = forms.CharField(widget=forms.PasswordInput())

# A user registration form for new users,staff , they have to be registered
class UserRegistrationForm(forms.ModelForm):
    password = forms.CharField(label='Password',widget=forms.PasswordInput())
    password2 = forms.CharField(label='Repeat password',widget=forms.PasswordInput())
    class Meta:
        model = User
        fields = ('username','first_name','email')

    def passlen(self):
        passdata = self.cleaned_data['password']
        if passdata.__len__() < 8:
            raise ValidationError('Password is too short')
        return passdata 

    def clean_password2(self):
        cd = self.cleaned_data
        if cd['password'] != cd['password2']:
            raise ValidationError('Passwords don\'t match')
        return cd['password2']

    def clean_email(self):
        cd = self.cleaned_data
        if  "@" not in  cd['email']:
            raise ValidationError('Enter a valid email address')
        return cd['email']


# For users who have been using the system , they can then edit their profiles 
class UserEditForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ('first_name','last_name','email')


# Profiles including additional data can also be edited
class ProfileEditForm(forms.ModelForm):
    class Meta:
        model = StaffProfiles
        fields = ('user','telnumber','address','photo')


#### ----- APP SPECIFIC FORMS i.e Incidences report, connect to stakeholders, pickup schedules, Harvest Details



class IncidenceReportForm(forms.ModelForm):
    class Meta:
        model = Incidences
        exclude = ['status']
        fields = ('email','phonenumber','incidence_type','incidence_description','nearest_town','location')
        widgets = {
            'location': GooglePointFieldWidget
        }

              

class PickupForm(forms.ModelForm):
    class Meta:
        model = PickupSchedules   
        fields = ('route_name','stakeholder','departure','stops','source')
        widgets = {
            'departure': DatePickerInput(),
        }     

class HarvestForm(forms.ModelForm):
    class Meta:
        model = HarvestDetails
        fields = ('date','fruits','weight')
        widgets = {
            'date' : DatePickerInput(),
        }        

"""
widgets = {
            'location':gis_forms.OSMWidget(
                attrs = {
                    'map_width':400,
                    'map_height':400,
                    'map_srid':4326,
                    'default_lon' :36.28007,
                    'default_lat':-0.91433, 
                    'default_zoom':7,
                }
            ),
        }  
"""