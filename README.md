# ug

Utils using Google API

To install:	```pip install ug```

You'll also need to get a [Google API key](https://support.google.com/googleapi/answer/6158862?hl=en)
and enable the maps services for it. 

When you call a function, in the `gmaps_client`, you can specify the key itself 
or can specify the environment variable (prefixed with `"$"`) where you stored it, 
or even a fully instantiated client you made yourself. 
If you don't specify anything, it will use `"$GOOGLE_API_KEY"` as the default 
(so will look for an API key in the `GOOGLE_API_KEY` environment variable).


# Examples

## Google maps

```python
>>> r = search_maps("meditation", "Aix-en-Provence", radius_in_meters=3000)
>>> len(r)
10
>>> [x['formatted_address'] for x in r]  # doctest: +SKIP
['90A Rue Jean Dausset, 13090 Aix-en-Provence, France',
'24 Rue Thiers, 13100 Aix-en-Provence, France',
...
'700 Chem. de Banon, 13100 Aix-en-Provence, France',
'31 Cr Gambetta 13100, 13090 Aix-en-Provence, France']
>>> r[0]  # doctest: +SKIP
'business_status': 'OPERATIONAL',
'formatted_address': '90A Rue Jean Dausset, 13090 Aix-en-Provence, France',
'geometry': {'location': {'lat': 43.53714249999999, 'lng': 5.4149873},
'viewport': {'northeast': {'lat': 43.53849157989272,
    'lng': 5.416325329892722},
'southwest': {'lat': 43.53579192010728, 'lng': 5.413625670107278}}},
'icon': 'https://maps.gstatic.com/mapfiles/place_api/icons/v1/png_71/school-71.png',
'icon_background_color': '#7B9EB0',
'icon_mask_base_uri': 'https://maps.gstatic.com/mapfiles/place_api/icons/v2/school_pinlet',
'name': 'Pleine conscience aix',
'opening_hours': {'open_now': True},
'photos': [{'height': 1067,
'html_attributions': ['<a href="https://maps.google.com/maps/contrib/114127511381087003840">A Google User</a>'],
'photo_reference': 'AdCG2DNSD6nzorLbQagoMyC_ATRfKWAtXYzDknmBYspoXGnJzeqxScNA3VIhF4wPKkAuI3W4KBOEvibZenNuO0qRVbNYkBFUahJSRPXJjtHFQj4nBur4auszmIwykM8QoMxcrHucGcwcYbj3GZnat1r6nDJXWAKrWLDEqbf9P4mVDoFIr7Vg',
'width': 1600}],
'place_id': 'ChIJbc-zeTeNyRIRrtgswndfJ34',
'plus_code': {'compound_code': 'GCP7+VX Aix-en-Provence',
'global_code': '8FM7GCP7+VX'},
'rating': 5,
'reference': 'ChIJbc-zeTeNyRIRrtgswndfJ34',
'types': ['school', 'health', 'point_of_interest', 'establishment'],
'user_ratings_total': 3}
```
