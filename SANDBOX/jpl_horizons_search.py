# https://astroquery.readthedocs.io/en/latest/jplhorizons/jplhorizons.html#

# sandbox script to test python's interface to JPL horizons https://ssd.jpl.nasa.gov/horizons/ (online solar system data and ephemeris computation service)

from astroquery.jplhorizons import Horizons

obj = Horizons(id='Ceres', location='568', epochs=2458133.33546)
print(obj)

statue_of_liberty = {'lon': -74.0466891,'lat': 40.6892534,'elevation': 0.093}
obj = Horizons(id='Ceres',location=statue_of_liberty,epochs=2458133.33546)
print(obj)

print(Horizons(id='Ceres').ephemerides())
print(Horizons(id='90000034', id_type=None).ephemerides()) # id='Encke' leads to ValueError: Ambiguous target name; provide unique id

obj = Horizons(id='Ceres', location='568',epochs={'start':'2010-01-01', 'stop':'2010-03-01','step':'10d'})
eph = obj.ephemerides()
print(eph)
