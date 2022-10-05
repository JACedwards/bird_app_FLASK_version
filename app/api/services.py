from app.models import User
from flask import jsonify, request, flash, redirect, url_for
from functools import wraps
from ebird.api import get_region, get_adjacent_regions, get_regions, get_observations
from flask_login import current_user

def token_required(api_route):
    @wraps(api_route)
    def decorator_function(*args, **kwargs):
        token = request.headers.get('birds-access-token')
        print(current_user.api_token)
        if not token:
            return jsonify({'Access Denied':'No API token.  Please sign up to recieve your api token'}), 401
        if not User.query.filter_by(api_token=token).first():
            return jsonify({'Invalid API token': 'Please check your API token or request a new one.'}), 403
        return api_route(*args, **kwargs)
    return decorator_function

#Had to abandon following this function when creating error handling.  Moved this code back into main function.

# def getCountyByDate(state_name, county_name, days):

#     """Call to API returning Bird observations for specified county ('county_name') and number of days from present backwards ('days')"""

#     state_code = get_regions('bdhdkslf0ktt', 'subnational1', 'US')
#     # print(state_code)
#     # above = dictionary of state codes

#     #Error Handling:  Check for missing/mispelled state:
#     miss_state = []
#     for y in state_code:
#         if y['name'] == state_name:
#             country_state = y['code']
#             # above = "US-NY" if New york put into form
#             miss_state.append(country_state)
#     print(miss_state)
  
    
#     county_code = get_regions('bdhdkslf0ktt', 'subnational2', f'{country_state}')
#     # print(county_code)
#     # dictionary of county codes

#     for x in county_code:
#         if x['name'] == county_name:
#             country_state_county = x['code']

#     records = get_observations('bdhdkslf0ktt', f'{country_state_county}', back=f"{days}")
#     # print(records)
#     return records




