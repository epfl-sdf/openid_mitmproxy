# Emulation d'un serveur Tequila via un serveur OpenID
# Petit Hello World pour se faire un auto connect sur Tequila
# 170912.1207

import collections
import re
import os
import errno
import csv
import json
import sys
import requests

from bs4 import BeautifulSoup
from version import __version__
from urllib.parse import urlparse
from urllib.request import Request, urlopen
#from urllib2 import urlopen

ORIG_URL = 'epfl.ch'
DEV_URL = 'dev-web-wordpress.epfl.ch'
SECTIONS_TO_REMOVE = ['recent-comments-2', 'archives-2', 'categories-2', 'meta-2', 'search-2']
LOGIN = 'wp-login.php'

TARGET_URLS = ['10.92.104.*', '*epfl.ch', '*wordpress*ch', 'localhost*', '0.0.0.0*']
WP_URLS = ['*web-wordpress.epfl.ch']
TQ_URLS = ['*tequila.epfl.ch']

COOKIE_FOLDER = 'data/cookies'
CREDENTIALS_FILE = '../credentials/credentials.csv'

SCRIPT_PATH = 'data/Scripts/'
TEMPLATE_PATH = 'data/Templates/'

print ("\n\nOn démarre la version: ",__version__,"\n")

def path_from_root(*x):
    return os.path.abspath(os.path.join(os.path.dirname(__file__), '..', *x))

with open(path_from_root("../ubuntu/emule_hello_world_1.secrets.json"), 'r') as f:
    secrets = json.loads(f.read())

print ("toto135208")

print (secrets)

print ("User: ", secrets["TQ_USER"])
print ("Pass: ", secrets["TQ_PASSWORD"])
zusername = secrets["TQ_USER"]
zpassword = secrets["TQ_PASSWORD"]
#sys.exit(0)

class Filter:

    def response(self, flow):
        url = flow.request.url
        print("------------url: ",url)

        zbranch = 'https://tequila.epfl.ch/cgi-bin/tequila/auth?requestkey='
        zlen = len(zbranch)
        zurl = url[:zlen]
        print("------------zurl: ",zurl)


        if not zurl == zbranch:
            return
        print("-----------yeah ça match !")

        print("---------- url: ." + url + ".")
        zrequestkey = url[zlen:]
        print("----------key: ." + zrequestkey + ".")

        yurl = "https://tequila.epfl.ch/cgi-bin/tequila/login"
        userAgent = 'Mozilla/5.0'
        saveCookies = COOKIE_FOLDER + '/' + 'cookie' + zrequestkey
        command = ('/usr/bin/wget --user-agent="' + userAgent + '"' + 
                ' --save-cookie="' + saveCookies + '"' +
                ' --keep-session-cookies' + 
                ' --delete-after' + 
                ' --max-redirect 0' + 
                ' "'+ yurl + '?username=' + zusername + '&password=' + zpassword + '&requestkey=' + zrequestkey + '" ' )
        xurl = yurl + '?username=' + zusername + '&password=' + zpassword + '&requestkey=' + zrequestkey + '\n'

        print("----------  commande: ." + command + ".")
        print("------------toto avant wget")
        os.system("" + command + "")
        print("------------toto après wget")






def start():
    return Filter()

#if __name__ == '__main__':
#    url1 = 'http://test-web-wordpress.epfl.ch/v1-testwp/briskenlab'
#    cookieFoldPath = 'data/cookies'
#    credFilePath = '../credentials/credentials.csv'
#    print(Filter.getCookie(url1, cookieFoldPath, credFilePath))



#Filter.getCredentials(None, os.path.abspath("../emule_hello_world_1.secrets.json"))
