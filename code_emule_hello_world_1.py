# Emulation d'un serveur Tequila via un serveur OpenID
# Petit Hello World pour se faire un auto connect sur Tequila
# 170913.1017

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

#from mitmproxy.models import HTTPResponse
#from netlib.http import Headers

ORIG_URL = 'epfl.ch'
DEV_URL = 'dev-web-wordpress.epfl.ch'
SECTIONS_TO_REMOVE = ['recent-comments-2', 'archives-2', 'categories-2', 'meta-2', 'search-2']
LOGIN = 'wp-login.php'

TARGET_URLS = ['10.92.104.*', '*epfl.ch', '*wordpress*ch', 'localhost*', '0.0.0.0*']
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

saveCookie = ""
zrequestkey = ""
class Filter:
    def makeHTTPCookiesFromWget(a):
        Domain = "."
        DefaultPath = "/"

        handler = open("data/cookies/cookiezvdf0h2c3mzvo8h1s827mg2v7fvxf7nx", "r")
        zcookie = handler.read()
        handler.close()
        listOfCookies = zcookie.split("\n")
        parsedCookies = ""

        for Cookie in listOfCookies:
            Parse = ""
            Parse = re.findall("([A-za-z._-]+)([ /\\t]+)(TRUE|FALSE)([ /\\t]+)(TRUE|FALSE)([ /\\t]+)([0-9]+)([ /\\t]+)(.*)([ /\\t]+)(.*)", Cookie)

            if len(Parse) != 1:
                continue

            ParsedLen = len(Parse[0])
            # validate cookie
            if ParsedLen == 10 or ParsedLen == 11:
                if ParsedLen == 10: # if cookie has no value
                    parsedCookies += Parse[0][8]+"=; "
                else:
                    parsedCookies += Parse[0][8]+"="+Parse[0][10]+"; "

        parsedCookies += "path="+DefaultPath+"; domain="+Domain+";"

        print(parsedCookies)
        return parsedCookies

    #auto-login django
    def request(self, flow):
        url = flow.request.url
        print("------------url: ",url)

        zbranch = 'https://tequila.epfl.ch/cgi-bin/tequila/auth?requestkey='
        zlen = len(zbranch)
        zurl = url[:zlen]
        print("------------zurl: ",zurl)


        if not zurl == zbranch:
            print("\n----------- request url: " + flow.request.url + "\n")
            return
        print("-----------yeah ça match !")

        print("---------- url: ." + url + ".")
        zrequestkey = url[zlen:]
        print("----------key: ." + zrequestkey + ".")

        yurl = "https://tequila.epfl.ch/cgi-bin/tequila/login"
        userAgent = 'Mozilla/5.0'
        saveCookie = COOKIE_FOLDER + '/' + 'cookie' + zrequestkey
        command = ('/usr/bin/wget --user-agent="' + userAgent + '"' + 
                ' --save-cookie="' + saveCookie + '"' +
                ' --keep-session-cookies' + 
                ' --delete-after' + 
                ' --max-redirect 0' + 
                ' "'+ yurl + '?username=' + zusername + '&password=' + zpassword + '&requestkey=' + zrequestkey + '" ' )
        xurl = yurl + '?username=' + zusername + '&password=' + zpassword + '&requestkey=' + zrequestkey + '\n'

        print("----------  commande: ." + command + ".")
        print("------------toto avant wget")
        os.system("" + command + "")
        print("------------toto après wget")

        print("------------ cookie file: " + saveCookie)
        f = open(saveCookie)
        zcookie = f.readlines()
        f.close()
        ycookie = zcookie[4]

        #print("------------ cookie contenu: " + zcookie[2])
        #print("------------ cookie line: " + ycookie)
        print ("------------ dir(flow): \n" + str(dir(flow)) )
        print ("------------ dir(flow.request): \n" + str(dir(flow.request)) )
        print ("------------ dir(flow.request.headers): \n" + str(dir(flow.request.headers)) )
        print ("------------ dir(flow.reply): \n" + str(dir(flow.reply)) )

        #flow.request.cookies = Filter.makeHTTPCookiesFromWget(saveCookie)
        #flow.request.host = '10.92.104.173'
        #flow.request.port = 8000
        #flow.request.path = '/logged?key=' + zrequestkey
        #flow.request.url = "http://10.92.104.173:8000/logged?key=" + zrequestkey


zf170913.1738
Malheureusement  la commande flow.reply n'existe plus dans la version 2.x 
Mais le principe est bien, on doit modifier la requête GET en une requête redirection 302, mais on ne sais pas comment le faire avec la version 2.x


        flow.reply(HTTPResponse('HTTP/1.1', 302, 'Found',
                                Headers(Location='http://10.92.104.173:8000/logged?key='  + zrequestkey,
                                        Content_Length='0'),
                                b''))





        print("\n----------- request url: " + flow.request.url + "\n")

    """ 
    def response(self, flow):
        url = flow.request.url

        zbranch = "http://10.92.104.173:8000/logged?key="
        zlen = len(zbranch)
        zurl = url[:zlen]

        if not zurl == zbranch:
            return
        print("-----------yeah ça match !")

        print("---------- url: ." + url + ".")

        #print("---------- dir(flow.response): \n " + str(dir(flow.response)))

        flow.response.headers['Location'] = "http://10.92.104.173:8000/logged?key=" + zrequestkey
        flow.response.headers['Set-Cookie'] = Filter.makeHTTPCookiesFromWget(saveCookie)
    """ 

def start():
    return Filter()

