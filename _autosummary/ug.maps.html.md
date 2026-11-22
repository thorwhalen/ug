# ug.maps

Google Maps tools.

### Functions

| [`acquire_maps_search_results_from_different_locations`](#ug.maps.acquire_maps_search_results_from_different_locations)(...)   | Acquire search results from different locations and store them.                               |
|--------------------------------------------------------------------------------------------------------------|-----------------------------------------------------------------------------------------------|
| [`get_latlon`](#ug.maps.get_latlon)(query, \*[, gmaps_client])                       | Get the latitude and longitude for a given query (address, city, etc.).                       |
| [`google_maps_url`](#ug.maps.google_maps_url)(query, \*[, zoom, maptype, ...])            | Generate a Google Maps URL for a location, directions, or a map view.                         |
| [`haversine_distance`](#ug.maps.haversine_distance)(latlon1, latlon2)                        | Calculate the distance between two points on the Earth's surface using the Haversine formula. |
| `identity`(x)                                                                                                |                                                                                               |
| [`maps_paged_results`](#ug.maps.maps_paged_results)(query, location_coords[, ...])           | Generator function to fetch paged results from the Google Maps API.                           |
| [`search_maps`](#ug.maps.search_maps)(query, center_location[, ...])                  | Retrieves the top `n_results` from Google Maps for a given search query and location.         |

### ug.maps.acquire_maps_search_results_from_different_locations(search_query, locations, \*, save_result, get_location=<function identity>, get_key=None, radius_in_meters=50000, raise_on_error=True, start_index=0, stop_index=None)

Acquire search results from different locations and store them.

#### NOTE
The function does NOT return the results, but a (possibly empty) list of
errors (if raise_on_error=False. The results are stored using the save_result
function. Users need to provide this function. Users may want to check out the
`dol` package and ecosystem for tools to make storing functions.

* **Parameters:**
  * **search_query** ([`str`](https://docs.python.org/3/builtins/stdtypes.html#str)) – The search term to query on Google Maps.
  * **locations** ([`Iterable`](https://docs.python.org/3/library/collections.abc.html#collections.abc.Iterable)[`LocationsSource`]) – The locations to search at.
  * **save_result** ([`Union`](https://docs.python.org/3/library/typing.html#typing.Union)[[`MutableMapping`](https://docs.python.org/3/library/collections.abc.html#collections.abc.MutableMapping), [`Callable`](https://docs.python.org/3/library/collections.abc.html#collections.abc.Callable)[[`KT`, [`Any`](https://docs.python.org/3/library/typing.html#typing.Any)], [`None`](https://docs.python.org/3/builtins/constants.html#None)]]) – A function to save the results.
  * **get_location** ([`Callable`](https://docs.python.org/3/library/collections.abc.html#collections.abc.Callable)[[`LocationsSource`], `Location`]) – A function to extract the location from the location source.
  * **get_key** ([`Callable`](https://docs.python.org/3/library/collections.abc.html#collections.abc.Callable)[[`LocationsSource`], `KT`] | [`None`](https://docs.python.org/3/builtins/constants.html#None)) – A function to extract the key from the location source.
  * **radius_in_meters** ([`int`](https://docs.python.org/3/builtins/functions.html#int)) – The search radius in meters.
  * **raise_on_error** ([`bool`](https://docs.python.org/3/builtins/functions.html#bool)) – Whether to raise an error if an exception occurs.
  * **start_index** ([`int`](https://docs.python.org/3/builtins/functions.html#int)) – The index to start at (inclusive).
  * **stop_index** ([`int`](https://docs.python.org/3/builtins/functions.html#int) | [`None`](https://docs.python.org/3/builtins/constants.html#None)) – The index to stop at (exclusive).
* **Return type:**
  [`list`](https://docs.python.org/3/builtins/stdtypes.html#list)

### ug.maps.get_latlon(query, , gmaps_client='$GOOGLE_API_KEY')

Get the latitude and longitude for a given query (address, city, etc.).

* **Return type:**
  [`tuple`](https://docs.python.org/3/builtins/stdtypes.html#tuple)[[`float`](https://docs.python.org/3/builtins/functions.html#float), [`float`](https://docs.python.org/3/builtins/functions.html#float)]

### ug.maps.google_maps_url(query, , zoom=15, maptype='roadmap', origin=None, destination=None, travelmode=None, waypoints=None, layer=None, place_id=None, street_view=False, heading=None, pitch=None, language=None, embed=False, iwloc=None)

Generate a Google Maps URL for a location, directions, or a map view.

* **Parameters:**
  * **query** ([`str`](https://docs.python.org/3/builtins/stdtypes.html#str) | [`tuple`](https://docs.python.org/3/builtins/stdtypes.html#tuple) | [`list`](https://docs.python.org/3/builtins/stdtypes.html#list) | [`dict`](https://docs.python.org/3/builtins/stdtypes.html#dict)) – Address, coordinates, or dictionary with ‘lat’ and ‘lon’.
  * **zoom** ([`int`](https://docs.python.org/3/builtins/functions.html#int)) – Zoom level (default is 15).
  * **maptype** ([`Literal`](https://docs.python.org/3/library/typing.html#typing.Literal)[`'roadmap'`, `'satellite'`, `'hybrid'`, `'terrain'`, `'google_earth'`]) – Type of map. One of ‘roadmap’, ‘satellite’, ‘hybrid’, ‘terrain’, ‘google_earth’.
  * **origin** ([`str`](https://docs.python.org/3/builtins/stdtypes.html#str)) – Starting location for directions.
  * **destination** ([`str`](https://docs.python.org/3/builtins/stdtypes.html#str)) – Destination for directions.
  * **travelmode** ([`Literal`](https://docs.python.org/3/library/typing.html#typing.Literal)[`'driving'`, `'walking'`, `'bicycling'`, `'transit'`]) – Mode of transportation: ‘driving’, ‘walking’, ‘bicycling’, or ‘transit’.
  * **waypoints** ([`list`](https://docs.python.org/3/builtins/stdtypes.html#list)[[`str`](https://docs.python.org/3/builtins/stdtypes.html#str)]) – Stops along the route.
  * **layer** ([`Literal`](https://docs.python.org/3/library/typing.html#typing.Literal)[`'bicycling'`, `'traffic'`, `'transit'`]) – Map overlay layer: ‘bicycling’, ‘traffic’, or ‘transit’.
  * **place_id** ([`str`](https://docs.python.org/3/builtins/stdtypes.html#str)) – Unique Place ID for a location.
  * **street_view** ([`bool`](https://docs.python.org/3/builtins/functions.html#bool)) – If True, show Street View.
  * **heading** ([`float`](https://docs.python.org/3/builtins/functions.html#float)) – Direction camera is pointing in Street View.
  * **pitch** ([`float`](https://docs.python.org/3/builtins/functions.html#float)) – Up/down angle of the camera in Street View.
  * **language** ([`str`](https://docs.python.org/3/builtins/stdtypes.html#str)) – Language code for the map interface.
  * **embed** ([`bool`](https://docs.python.org/3/builtins/functions.html#bool)) – If True, generate embeddable map.
  * **iwloc** ([`str`](https://docs.python.org/3/builtins/stdtypes.html#str)) – Center the map on a specific pin or location.
* **Returns:**
  A fully constructed Google Maps URL.
* **Return type:**
  [`str`](https://docs.python.org/3/builtins/stdtypes.html#str)

### Examples

```pycon
>>> google_maps_url({'lat': 43.5300401, 'lon': 5.4229452})
'https://www.google.com/maps?q=43.5300401,5.4229452&z=15&t=m'
```

```pycon
>>> google_maps_url((43.5300401, 5.4229452), zoom=16, maptype='satellite', layer='traffic')
'https://www.google.com/maps?q=43.5300401,5.4229452&z=16&t=k&layer=t'
```

```pycon
>>> google_maps_url('some address', street_view=True, heading=90)
'https://www.google.com/maps?q=some+address&z=15&t=m&cbll=some+address&cbp=12,90,0,0,5,0'
```

### ug.maps.haversine_distance(latlon1, latlon2)

Calculate the distance between two points on the Earth’s surface using the Haversine formula.

The Haversine formula accounts for the Earth’s curvature, making it suitable for calculating
the great-circle distance between two geographic coordinates (latitude and longitude) in meters.

### Parameters

latlon1:
: Tuple of latitude and longitude of the first point in decimal degrees.

latlon2: float
: Tuple of latitude and longitude of the second point in decimal degrees.

### Returns

float
: Distance between the two points in meters.

Explanation:

1. The radius of the Earth (R) is approximately 6,371,000 meters.
2. Convert latitudes and longitudes from degrees to radians, since trigonometric functions in
   Python’s math library operate in radians.
3. The Haversine formula calculates the great-circle distance:
   - ‘a’ is the square of half the chord length between the points.
   - ‘c’ is the angular distance in radians.
4. Multiply ‘c’ by the Earth’s radius to get the distance in meters.

Example usage:

```pycon
>>> # Paris to New York
>>> haversine_distance((48.8566, 2.3522), (40.7128, -74.0060))
5837240.90...
>>> # San Francisco to Los Angeles
>>> haversine_distance([37.7749, -122.4194], [34.0522, -118.2437])
559120.57...
>>>  # Same location (London)
>>> haversine_distance((51.5074, -0.1278), (51.5074, -0.1278))
0.0
```

### ug.maps.maps_paged_results(query, location_coords, radius_in_meters=50000, , gmaps_client='$GOOGLE_API_KEY', seconds_between_requests=2)

Generator function to fetch paged results from the Google Maps API.

* **Parameters:**
  * **query** ([`str`](https://docs.python.org/3/builtins/stdtypes.html#str)) – The search term to query on Google Maps.
  * **location_coords** ([`tuple`](https://docs.python.org/3/builtins/stdtypes.html#tuple)[[`float`](https://docs.python.org/3/builtins/functions.html#float), [`float`](https://docs.python.org/3/builtins/functions.html#float)]) – Coordinates (latitude, longitude) to bias the search towards.
  * **radius_in_meters** ([`int`](https://docs.python.org/3/builtins/functions.html#int)) – The search radius in meters.
  * **gmaps_client** ([`Union`](https://docs.python.org/3/library/typing.html#typing.Union)[[`str`](https://docs.python.org/3/builtins/stdtypes.html#str), `Client`, [`None`](https://docs.python.org/3/builtins/constants.html#None)]) – An instance of the Google Maps client.
  * **seconds_between_requests** ([`int`](https://docs.python.org/3/builtins/functions.html#int)) – Seconds to wait between paginated requests.
* **Yields:**
  *List[Dict[str, Any]]* – A list of place results from each page.
* **Return type:**
  [*Generator*](https://docs.python.org/3/library/collections.abc.html#collections.abc.Generator)[[*list*](https://docs.python.org/3/builtins/stdtypes.html#list)[[*dict*](https://docs.python.org/3/builtins/stdtypes.html#dict)[[*str*](https://docs.python.org/3/builtins/stdtypes.html#str), [*Any*](https://docs.python.org/3/library/typing.html#typing.Any)]], *None*, *None*]

### ug.maps.search_maps(query, center_location, radius_in_meters=50000, , gmaps_client='$GOOGLE_API_KEY', n_results=10, seconds_between_requests=2)

Retrieves the top `n_results` from Google Maps for a given search query and location.

* **Parameters:**
  * **query** ([`str`](https://docs.python.org/3/builtins/stdtypes.html#str)) – The search term to query on Google Maps.
  * **center_location** ([`str`](https://docs.python.org/3/builtins/stdtypes.html#str) | [`tuple`](https://docs.python.org/3/builtins/stdtypes.html#tuple)[[`float`](https://docs.python.org/3/builtins/functions.html#float), [`float`](https://docs.python.org/3/builtins/functions.html#float)] | [`list`](https://docs.python.org/3/builtins/stdtypes.html#list)[[`float`](https://docs.python.org/3/builtins/functions.html#float)]) – 

    The location to bias the search towards.
    - If a string, it’s treated as a city name and geocoded to coordinates.
    - If a tuple/list of floats, it’s used directly as (latitude, longitude).
  * **radius_in_meters** ([`int`](https://docs.python.org/3/builtins/functions.html#int)) – The search radius in meters (default is 50,000).
  * **gmaps_client** ([`Union`](https://docs.python.org/3/library/typing.html#typing.Union)[[`str`](https://docs.python.org/3/builtins/stdtypes.html#str), `Client`, [`None`](https://docs.python.org/3/builtins/constants.html#None)]) – An instance of the Google Maps client. If None, a new client will be created.
  * **n_results** ([`int`](https://docs.python.org/3/builtins/functions.html#int)) – The number of top results to return (default is 10).
  * **seconds_between_requests** ([`int`](https://docs.python.org/3/builtins/functions.html#int)) – Seconds to wait between paginated requests (default is 2).
* **Returns:**
  A list of dictionaries containing details about each place.
* **Return type:**
  [`list`](https://docs.python.org/3/builtins/stdtypes.html#list)[[`dict`](https://docs.python.org/3/builtins/stdtypes.html#dict)[[`str`](https://docs.python.org/3/builtins/stdtypes.html#str), [`Any`](https://docs.python.org/3/library/typing.html#typing.Any)]]
* **Raises:**
  * [**ValueError**](https://docs.python.org/3/builtins/exceptions.html#ValueError) – If the city name cannot be geocoded or coordinates are invalid.
  * [**TypeError**](https://docs.python.org/3/builtins/exceptions.html#TypeError) – If `center_location` is neither a string nor a tuple/list of two floats.

### Examples

```pycon
>>> r = search_maps("meditation", "Aix-en-Provence", radius_in_meters=3000)
>>> len(r)
10
>>> [x['formatted_address'] for x in r]
['90A Rue Jean Dausset, 13090 Aix-en-Provence, France',
'24 Rue Thiers, 13100 Aix-en-Provence, France',
...
'700 Chem. de Banon, 13100 Aix-en-Provence, France',
'31 Cr Gambetta 13100, 13090 Aix-en-Provence, France']
>>> r[0]
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
