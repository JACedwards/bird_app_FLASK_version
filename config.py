# setting up and organize application file structure and configuration
# includes what secret variables and where is the base/root folder
# we will need help from the os package

import os

# set up base directory of entire application

basedir = os.path.abspath(os.path.dirname(__name__))


#set upu class for our configuaration variables

class Config:

    """Setting configuation variables that tell flask how to run"""
    # NONE OF NEXT should be public info
        # so theira acutal value is in .env file
        # value here will just be function cal to .env file

    FLASK_APP = os.environ.get('FLASK_APP') 
    FLASK_ENV = os.environ.get('FLASK_ENV')
    SECRET_KEY = os.environ.get('FLASK_KEY')
