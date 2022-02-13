from re import search
from django.contrib import admin
from django.contrib.gis.admin import OSMGeoAdmin
from leaflet.admin import LeafletGeoAdmin

from geoapp.models import Constituency, StaffProfiles, Stakeholders, Fertilizers, Incidences, Companies
from geoapp.models import HarvestDetails, Seedlings, PruningCare, PickupSchedules


@admin.register(Constituency)
class ConstituencyAdmin(LeafletGeoAdmin):
    list_display = ('const_nam','county_nam','shape_area')
    list_filter = ('const_nam','county_nam','shape_area')
    search_fields = ('const_nam','county_nam','shape_area')

@admin.register(Stakeholders)
class StakeholdersAdmin(admin.ModelAdmin):
    list_display = ('name','email','telephone','dealer')
    list_filter =  ('name','email','telephone','dealer')
    search_fields = ('name','email','telephone','dealer')


@admin.register(Companies)
class CompaniesAdmin(OSMGeoAdmin):
    list_display = ('company_na','address')
    list_filter = ('company_na','address')
    search_fields = ('company_na','address')


@admin.register(Fertilizers)
class FertilizerAdmin(admin.ModelAdmin):
    list_display = ('name','weight','description','price')
    list_filter = ('name','weight','description','price')
    search_fields = ('name','weight','description','price')

@admin.register(Incidences)  
class IncidencesAdmin(LeafletGeoAdmin):
    list_display = ('incidence_date','incidence_type','status')
    list_filter = ('incidence_date','incidence_type','status')
    search_fields = ('incidence_date','incidence_type','status')

@admin.register(PickupSchedules)
class SchedulesAdmin(admin.ModelAdmin):
    list_display = ('route_name','stakeholder','departure','stops','source')
    list_filter = ('route_name','stakeholder','departure','stops','source')
    search_fields = ('route_name','stakeholder','departure','stops','source')

@admin.register(Seedlings)
class SeedlingsAdmin(admin.ModelAdmin):
    list_display = ('cultivar','description','price')
    list_filter = ('cultivar','description','price')
    search_fields = ('cultivar','description','price')

@admin.register(PruningCare)
class PruningAdmin(admin.ModelAdmin):
    list_display = ('method','description')
    list_filter = ('method','description')
    search_fields = ('method','description')
