from django.urls import path, include
from geoapp import views
from django.contrib.auth import views as auth_views
from django.contrib import admin

admin.site.site_header = "Nakuru Avocado Net"
admin.site.site_title = "Nakuru Avocado Net Admin Portal"
admin.site.index_title = "Nakuru Avocado Net App"



urlpatterns = [

    ### Pages
    path('',views.Gisnet_home.as_view(), name='home'),
    path('reporting/',views.Gisnet_reporter.as_view(),name='reporting'),
    path('plantcare/',views.Gisnet_plantcare.as_view(),name='plantcare'),


    #### Authentication VIEWS
    path('login/',views.login_view,name='login'),
    path('logout/',auth_views.LogoutView.as_view(),name='logout'),
    path('deactivated/',views.deactivate,name='deactivated'),
    path('password_reset/',auth_views.PasswordResetView.as_view(),name='password_reset'),
    path('password_reset/done/',auth_views.PasswordResetDoneView.as_view(),name='password_reset_done'),
    path('reset/<uidb64>/<token>/',auth_views.PasswordResetConfirmView.as_view(),name='password_reset_confirm'),
    path('reset/done/',auth_views.PasswordResetCompleteView.as_view(),name='password_reset_complete'),
    path('register/',views.register,name='register'),
    path('edit_profile/',views.edit_profile,name='edit_profile'),

    ##path('reports_form/',views.incidence_form,name='reports_form'),
    
    path('harvest_details/',views.harvest_form,name='harvest_details'),

    path('constituen/',views.get_constituency, name='constituen'),
    path('companies/',views.get_companies,name='companies'),
]