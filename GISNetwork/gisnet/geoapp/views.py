from django.shortcuts import render, redirect, render_to_response
from django.http import HttpResponse, HttpResponseRedirect
from django.template import context
from django.views.generic import TemplateView, CreateView
from django.views.generic.edit import FormView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout
from django.core.serializers import serialize
from django.contrib import messages
from django.urls import reverse, resolve
import logging
import traceback
from django.core.mail import send_mail
from geoapp.models import Constituency, StaffProfiles, Stakeholders, Fertilizers, Incidences, Companies
from geoapp.models import HarvestDetails, Seedlings, PruningCare, PickupSchedules
from geoapp.forms import LoginForm, UserEditForm, UserRegistrationForm, ProfileEditForm
from geoapp.forms import IncidenceReportForm, HarvestForm

logger = logging.getLogger(__name__)




"""
Template views in Django should be used for GET requests, they are not meant for handling forms but
just rendering templates
"""

class Gisnet_home(LoginRequiredMixin, TemplateView):
    template_name = 'index.html'
    login_url = '/login/'


### This form allows the use to post details on the incident encountered

class Gisnet_reporter(LoginRequiredMixin, CreateView):
    template_name = 'reporter.html'
    login_url = '/login/'   

    def get(self,request,*args,**kwargs):
        context = {'form':IncidenceReportForm()}
        return render(request,'reporter.html',context)

    def post(self, request, *args, **kwargs):
        form = IncidenceReportForm(request.POST)
        if form.is_valid():
            incident = form.save()
            incident.save()
            messages.success(request,'Case has been reported, wait for reply')
            return HttpResponseRedirect('/reporting/')
        else:
            messages.error(request,'Invalid details submitted')
        return render(request,'reporter.html',{'form':form})            



class Gisnet_plantcare(LoginRequiredMixin, TemplateView):
    template_name = 'plantcare.html'
    login_url = '/login/'



#### ------ USER AUTHENTICATION VIEWS ------- #####

def login_view(request):
    # on receiving a post request
    if request.method == 'POST':
        login_form = LoginForm(data=request.POST)
        if login_form.is_valid():
            cd = login_form.cleaned_data
            user = authenticate(request,username=cd['username'],password=cd['password'])
            if user is not None:
                if user.is_active:
                    if user.is_staff:
                        login(request,user)
                        return HttpResponseRedirect('/admin/')
                    else:    
                        login(request,user)
                        return HttpResponseRedirect('/')
                else:
                    return HttpResponseRedirect('/deactivated/')
            else:
                messages.error(request,'Your credentials are not correct, check again all the fields')
    
    # when the form is initially rendered
    else:
        login_form = LoginForm()   
    return render(request,'registration/login.html',{'login_form':login_form })                      

@login_required
def logout_view(request):
    logout(request)
    return HttpResponseRedirect('/logout/') 

def deactivate(request):
    return render(request,'registration/deactivated.html',{})


def register(request):
    if request.method == 'POST':
        register_form = UserRegistrationForm(request.POST)
        if register_form.is_valid():
            new_user = register_form.save(commit=False)
            # set password as given by the user
            new_user.set_password(register_form.cleaned_data['password'])
            # Now save the User object
            new_user.save()

            # Also create a new profile instance associated with this user 
            StaffProfiles.objects.create(user=new_user)
            return render(request,'registration/register_done.html',{'new_user':new_user})
    else:
        register_form = UserRegistrationForm()
    return render(request,'registration/register.html',{'register_form':register_form})            

@login_required
def edit_profile(request):
    if request.method == 'POST':
        user_form = UserEditForm(data=request.POST,instance=request.user)
        profile_form = ProfileEditForm(data=request.POST,files=request.FILES,instance=request.user.staffprofiles)
        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile_form.save()
            messages.success(request,'User profile updated successfully')
        else:
            messages.error(request,'Error while updating profile')
    else:
        user_form = UserEditForm(instance=request.user)
        profile_form = ProfileEditForm(instance=request.user.staffprofiles) 
    return render(request,'registration/edit_profile.html',{'user_form':user_form,'profile_form':profile_form})       



#####------ Incidences Reporting Form --------####

"""
@login_required
def incidence_form(request):
    if request.method == "POST":
        report = None
        report_form = IncidenceReportForm(data=request.POST)
        if report_form.is_valid():
            report = report_form.save(commit=True)
            messages.success('Your incidence has been received successfully')
            return HttpResponseRedirect('/reporting/')
        else:
            messages.error("Check the form fields again")
    else:
        report_form = IncidenceReportForm()
    return render(request,'reporter.html',{'report_form':report_form}) 

"""           

@login_required
def harvest_form(request):
    data = HarvestDetails.objects.all()
    if request.method == "POST":
        havst_form = HarvestForm(data=request.POST)
        if havst_form.is_valid():
            havst_form.save(commit=True)
            messages.success(request,'Harvest details have been added successfully')
            return redirect('/harvest_details/')
        else:
            messages.error(request,"Make sure all form fields are filled!")
    else:
        havst_form = HarvestForm()

    context = {
        'data':data,
        'havst_form':havst_form,
    }        
    return render(request,'harvests_details.html',context)                


### ----- Geo Data VIEWS --------#######
def get_constituency(reqest):
    cons_data = serialize('geojson',Constituency.objects.all())
    return HttpResponse(cons_data,content_type='json')

def get_companies(request):
    comps = serialize('geojson',Companies.objects.all())
    return HttpResponse(comps,content_type='json')



## Check this list view again
def get_schedules(request):
    schedules = PickupSchedules.objects.all()
    return HttpResponse(schedules)



