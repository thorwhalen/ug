"""Google Maps tools."""

import time
import itertools
from functools import partial
from typing import (
    Any,
    Dict,
    List,
    Tuple,
    Union,
    Generator,
    Callable,
    Optional,
    KT,
    Iterable,
    TypeVar,
)
from lkj import print_progress

from ug.util import ensure_gmaps_client, ClientSpec, DFLT_GOOGLE_API_KEY_ENV_VAR

DFLT_RADIUS_IN_METERS = 50000  # in meters


LocationsSource = TypeVar('LocationsSource')
Location = TypeVar('Location')


def identity(x):
    return x


def acquire_maps_search_results_from_different_locations(
    search_query: str,
    locations: Iterable[LocationsSource],
    *,
    save_result: Callable[[KT, dict], Any],
    get_location: Callable[[LocationsSource], Location] = identity,
    get_key: Optional[Callable[[LocationsSource], KT]] = None,
    radius_in_meters: int = DFLT_RADIUS_IN_METERS,
    raise_on_error: bool = True,
) -> list:
    """
    Acquire search results from different locations and store them.

    Note: The function does NOT return the results, but a (possibly empty) list of
    errors (if raise_on_error=False. The results are stored using the save_result
    function. Users need to provide this function. Users may want to check out the
    `dol` package and ecosystem for tools to make storing functions.

    Parameters:
        search_query (str): The search term to query on Google Maps.
        locations (Iterable[LocationsSource]): The locations to search at.
        save_result (Callable[[KT, dict], Any]): A function to save the results.
        get_location (Callable[[LocationsSource], Location]): A function to extract the location from the location source.
        get_key (Optional[Callable[[LocationsSource], KT]]): A function to extract the key from the location source.
        radius_in_meters (int): The search radius in meters.

    """
    clog = partial(print_progress, refresh=True)

    def _get_key(i, location):
        if get_key:
            return get_key(location)
        else:
            return i

    def search_results_gen():
        location = None  # just to avoid UnboundLocalError
        for i, location_src in enumerate(locations):
            try:
                location = get_location(location_src)  # extract location
                key = _get_key(i, location_src)  # extract key
                clog(f"{i:04.0f}: {key}")
                # search the query at that location
                r = search_maps(
                    search_query, location, radius_in_meters=radius_in_meters
                )
                save_result(key, r)  # save the results
            except Exception as e:
                if raise_on_error:
                    raise
                yield dict(i=i, location=location, e=e)
                print(f"ERROR: {e}")

    errors = list(search_results_gen())
    print(f"Number of errors: {len(errors)}")

    return errors


def search_maps(
    query: str,
    center_location: Union[str, Tuple[float, float], List[float]],
    radius_in_meters: int = DFLT_RADIUS_IN_METERS,
    *,
    gmaps_client: ClientSpec = DFLT_GOOGLE_API_KEY_ENV_VAR,
    n_results: int = 10,
    seconds_between_requests: int = 2,
) -> List[Dict[str, Any]]:
    """
    Retrieves the top `n_results` from Google Maps for a given search query and location.

    Parameters:
        query (str): The search term to query on Google Maps.
        center_location (Union[str, Tuple[float, float], List[float]]): The location to bias the search towards.
            - If a string, it's treated as a city name and geocoded to coordinates.
            - If a tuple/list of floats, it's used directly as (latitude, longitude).
        radius_in_meters (int): The search radius in meters (default is 50,000).
        gmaps_client (optional): An instance of the Google Maps client. If None, a new client will be created.
        n_results (int): The number of top results to return (default is 10).
        seconds_between_requests (int): Seconds to wait between paginated requests (default is 2).

    Returns:
        List[Dict[str, Any]]: A list of dictionaries containing details about each place.

    Raises:
        ValueError: If the city name cannot be geocoded or coordinates are invalid.
        TypeError: If `center_location` is neither a string nor a tuple/list of two floats.


    Examples:

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
    """

    gmaps_client = ensure_gmaps_client(gmaps_client)

    # Determine the coordinates for the specified location
    if isinstance(center_location, str):
        # Geocode the city name to get coordinates
        geocode_result = gmaps_client.geocode(center_location)
        if geocode_result:
            location = geocode_result[0]['geometry']['location']
            location_coords = (location['lat'], location['lng'])
        else:
            raise ValueError(f"Could not find location for: {center_location}")
    elif isinstance(center_location, (tuple, list)) and len(center_location) == 2:
        # Use the provided coordinates directly
        try:
            location_coords = (float(center_location[0]), float(center_location[1]))
        except (ValueError, TypeError):
            raise ValueError("Coordinates must be numeric values.")
    else:
        raise TypeError(
            "center_location must be a string (city name) or a tuple/list of (latitude, longitude)."
        )

    # Use the generator function to fetch results
    result_generator = maps_paged_results(
        query=query,
        location_coords=location_coords,
        radius_in_meters=radius_in_meters,
        gmaps_client=gmaps_client,
        seconds_between_requests=seconds_between_requests,
    )

    # Gather results up to n_results
    results = list(
        itertools.islice(itertools.chain.from_iterable(result_generator), n_results)
    )

    return results


def maps_paged_results(
    query: str,
    location_coords: Tuple[float, float],
    radius_in_meters: int = DFLT_RADIUS_IN_METERS,
    *,
    gmaps_client: ClientSpec = DFLT_GOOGLE_API_KEY_ENV_VAR,
    seconds_between_requests: int = 2,
) -> Generator[List[Dict[str, Any]], None, None]:
    """
    Generator function to fetch paged results from the Google Maps API.

    Parameters:
        query (str): The search term to query on Google Maps.
        location_coords (Tuple[float, float]): Coordinates (latitude, longitude) to bias the search towards.
        radius_in_meters (int): The search radius in meters.
        gmaps_client: An instance of the Google Maps client.
        seconds_between_requests (int): Seconds to wait between paginated requests.

    Yields:
        List[Dict[str, Any]]: A list of place results from each page.
    """
    radius_in_meters = int(radius_in_meters)
    # Initial search request
    response = gmaps_client.places(
        query=query,
        location=location_coords,
        radius=radius_in_meters,
    )

    yield response.get('results', [])

    # Handle pagination
    while 'next_page_token' in response:
        time.sleep(seconds_between_requests)
        response = gmaps_client.places(
            query=query,
            page_token=response['next_page_token'],
            location=location_coords,
            radius=radius_in_meters,
        )
        yield response.get('results', [])


# -------------------------------------------------------------------------------------
# Geo utils

import math


def haversine_distance(latlon1, latlon2):
    """
    Calculate the distance between two points on the Earth's surface using the Haversine formula.

    The Haversine formula accounts for the Earth's curvature, making it suitable for calculating
    the great-circle distance between two geographic coordinates (latitude and longitude) in meters.

    Parameters:
    latlon1:
        Tuple of latitude and longitude of the first point in decimal degrees.
    latlon2: float
        Tuple of latitude and longitude of the second point in decimal degrees.

    Returns:
    float
        Distance between the two points in meters.

    Explanation:
    1. The radius of the Earth (R) is approximately 6,371,000 meters.
    2. Convert latitudes and longitudes from degrees to radians, since trigonometric functions in
       Python's math library operate in radians.
    3. The Haversine formula calculates the great-circle distance:
       - 'a' is the square of half the chord length between the points.
       - 'c' is the angular distance in radians.
    4. Multiply 'c' by the Earth's radius to get the distance in meters.

    Example usage:

    >>> # Paris to New York
    >>> haversine_distance((48.8566, 2.3522), (40.7128, -74.0060))  # doctest: +ELLIPSIS
    5837240.90...
    >>> # San Francisco to Los Angeles
    >>> haversine_distance([37.7749, -122.4194], [34.0522, -118.2437])  # doctest: +ELLIPSIS
    559120.57...
    >>>  # Same location (London)
    >>> haversine_distance((51.5074, -0.1278), (51.5074, -0.1278))
    0.0
    """
    lat1, lon1 = latlon1
    lat2, lon2 = latlon2

    # Radius of the Earth in meters
    R = 6371000

    # Convert latitudes and longitudes from degrees to radians
    phi1 = math.radians(lat1)
    phi2 = math.radians(lat2)
    delta_phi = math.radians(lat2 - lat1)
    delta_lambda = math.radians(lon2 - lon1)

    # Haversine formula
    a = (
        math.sin(delta_phi / 2) ** 2
        + math.cos(phi1) * math.cos(phi2) * math.sin(delta_lambda / 2) ** 2
    )
    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))

    # Distance in meters
    distance = R * c

    return distance


# import time

# from ug.util import ensure_gmaps_client


# DFLT_RADIUS_IN_METERS = 50000  # in meters


# def google_maps_search(
#     query,
#     center_location,
#     radius_in_meters=DFLT_RADIUS_IN_METERS,
#     *,
#     gmaps_client=None,
#     n_results: int = 10,
#     seconds_between_requests: int = 2,
# ):
#     """
#     Retrieves the top n results from Google Maps for a given search query and city.

#     Parameters:
#         query (str): The search term to query on Google Maps.
#         center_location (str): The name of the city to bias the search towards.
#         n (int): The number of top results to return (default is 10).

#     Returns:
#         list: A list of dictionaries containing details about each place.
#     """

#     gmaps_client = ensure_gmaps_client(gmaps_client)

#     # Determine the coordinates for the specified location
#     if isinstance(center_location, str):
#         # Geocode the city name to get coordinates
#         geocode_result = gmaps_client.geocode(center_location)
#         if geocode_result:
#             location = geocode_result[0]['geometry']['location']
#             location_coords = (location['lat'], location['lng'])
#         else:
#             print(f"Could not find location for: {center_location}")
#             return []
#     elif (
#         isinstance(center_location, tuple) or isinstance(center_location, list)
#     ) and len(center_location) == 2:
#         # Use the provided coordinates directly
#         try:
#             location_coords = (float(center_location[0]), float(center_location[1]))
#         except ValueError:
#             print("Coordinates must be numeric values.")
#             return []
#     else:
#         print(
#             "center_location must be a string (city name) or a tuple/list of (latitude, longitude)."
#         )
#         return []

#     # Perform the text search with location bias towards the specified location
#     response = gmaps_client.places(
#         query=query,
#         location=location_coords,
#         radius=radius_in_meters,  # Adjust radius as needed
#     )

#     results = response.get('results', [])

#     while 'next_page_token' in response and len(results) < n_results:
#         time.sleep(seconds_between_requests)
#         response = gmaps_client.places(
#             query=query,
#             page_token=response['next_page_token'],
#             location=location_coords,
#             radius=radius_in_meters,
#         )
#         results.extend(response.get('results', []))

#     return results[:n_results]
