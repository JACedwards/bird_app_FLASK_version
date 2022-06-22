from app.models import User
from flask import jsonify, request
from functools import wraps
from ebird.api import get_region, get_adjacent_regions, get_regions, get_observations

def token_required(api_route):
    @wraps(api_route)
    def decorator_function(*args, **kwargs):
        token = request.headers.get('birds-access-token')
        if not token:
            return jsonify({'Access Denied':'No API token.  Please sign up to recieve your api token'}), 401
        if not User.query.filter_by(api_token=token).first():
            return jsonify({'Invalid API token': 'Please check your API token or request a new one.'}), 403
        return api_route(*args, **kwargs)
    return decorator_function

def getCountyByDate(county_name, days):

    """Call to API returning Bird observations for specified county ('county_name') and number of days from present backwards ('days')"""

    county_code = get_regions('bdhdkslf0ktt', 'subnational2', 'US-IN')

    for x in county_code:
        if x['name'] == county_name:
            country_state_county = x['code']

    records = get_observations('bdhdkslf0ktt', f'{country_state_county}', back=f"{days}")
    return records