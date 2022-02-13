from django.contrib.gis.utils import LayerMapping
import os
from geoapp.models import Constituency, Companies




# Auto-generated `LayerMapping` dictionary for constituency model
constituency_mapping = {
    'objectid': 'objectid',
    'const_nam': 'const_nam',
    'const_no': 'const_no',
    'county_nam': 'county_nam',
    'st_area_sh': 'st_area_sh',
    'st_length_field': 'st_length_',
    'shape_leng': 'Shape_Leng',
    'shape_area': 'Shape_Area',
    'globalid': 'GlobalID',
    'geom': 'MULTIPOLYGON',
}
cons_shp = os.path.abspath(os.path.join(os.path.dirname(__file__),'data','constituency.shp'),)
def run_const(verbose=True):
    lm = LayerMapping(Constituency,cons_shp,constituency_mapping,transform=False)
    lm.save(strict=True,verbose=verbose)

# Auto-generated `LayerMapping` dictionary for Companies model
companies_mapping = {
    'company_na': 'Company_na',
    'address': 'Address',
    'lat': 'Lat',
    'long': 'Long',
    'geom': 'POINT',
}
comp_shp = os.path.abspath(os.path.join(os.path.dirname(__file__),'data','Company_locations.shp'))
def run_companies(verbose=True):
    lm = LayerMapping(Companies,comp_shp,companies_mapping)
    lm.save(strict=True,verbose=verbose)