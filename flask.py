from flask import Flask, render_template, request 
import pickle
import numpy as np 
import re
from urllib.parse import urlparse
from tld import get_tld 

app = Flask(__name__)

# Load the models
with open('models/sms_model.pkl', 'rb') as f:
    sms_model = pickle.load(f)

with open('models/url_model.pkl', 'rb') as f:
    url_model = pickle.load(f)

# Functions for URL feature extraction (include necessary feature extraction functions here)
def count_www(url):
    return url.count('www')

def count_atrate(url):
    return url.count('@')

def no_of_dir(url):
    urldir = urlparse(url).path
    return urldir.count('/')

def no_of_embed(url):
    urldir = urlparse(url).path
    return urldir.count('//')

def shortening_service(url):
    match = re.search('bit\.ly|goo\.gl|shorte\.st|go2l\.ink|x\.co|ow\.ly|t\.co|tinyurl|tr\.im|is\.gd|cli\.gs|'
                      'yfrog\.com|migre\.me|ff\.im|tiny\.cc|url4\.eu|twit\.ac|su\.pr|twurl\.nl|snipurl\.com|'
                      'short\.to|BudURL\.com|ping\.fm|post\.ly|Just\.as|bkite\.com|snipr\.com|fic\.kr|loopt\.us|'
                      'doiop\.com|short\.ie|kl\.am|wp\.me|rubyurl\.com|om\.ly|to\.ly|bit\.do|t\.co|lnkd\.in|'
                      'db\.tt|qr\.ae|adf\.ly|goo\.gl|bitly\.com|cur\.lv|tinyurl\.com|ow\.ly|bit\.ly|ity\.im|'
                      'q\.gs|is\.gd|po\.st|bc\.vc|twitthis\.com|u\.to|j\.mp|buzurl\.com|cutt\.us|u\.bb|yourls\.org|'
                      'x\.co|prettylinkpro\.com|scrnch\.me|filoops\.info|vzturl\.com|qr\.net|1url\.com|tweez\.me|v\.gd|'
                      'tr\.im|link\.zip\.net', url)
    return 1 if match else 0

def count_http(url):
    return url.count('http')

def count_https(url):
    return url.count('https')

def count_per(url):
    return url.count('%')

def count_ques(url):
    return url.count('?')

def count_hyphen(url):
    return url.count('-')

def count_equal(url):
    return url.count('=')

def url_length(url):
    return len(str(url))

def hostname_length(url):
    return len(urlparse(url).netloc)

def suspicious_words(url):
    match = re.search('PayPal|login|signin|bank|account|update|free|lucky|service|bonus|ebayisapi|webscr', url)
    return 1 if match else 0

def digit_count(url):
    return sum(c.isnumeric() for c in url)

def letter_count(url):
    return sum(c.isalpha() for c in url)

def fd_length(url):
    urlpath = urlparse(url).path
    try:
        return len(urlpath.split('/')[1])
    except:
        return 0

def tld_length(tld):
    try:
        return len(tld)
    except:
        return -1

def count_dot(url):
    return url.count('.')

def google_index(url):
    # Simulate a google search check, return 1 if found
    return 1

def having_ip_address(url):
    match = re.search('(([01]?\\d\\d?|2[0-4]\\d|25[0-5])\\.([01]?\\d\\d?|2[0-4]\\d|25[0-5])\\.([01]?\\d\\d?|2[0-4]\\d|25[0-5])\\.'
                      '([01]?\\d\\d?|2[0-4]\\d|25[0-5])\\/)|'
                      '((0x[0-9a-fA-F]{1,2})\\.(0x[0-9a-fA-F]{1,2})\\.(0x[0-9a-fA-F]{1,2})\\.(0x[0-9a-fA-F]{1,2})\\/)' # IPv4 in 16-bit format
                      '(?:[a-fA-F0-9]{1,4}:){7}[a-fA-F0-9]{1,4}', url)
    return 1 if match else 0

def abnormal_url(url):
    hostname = urlparse(url).hostname
    hostname = str(hostname)
    match = re.search(hostname, url)
    return 1 if match else 0

def get_url_features(url):
    status = []
    status.append(having_ip_address(url))
    status.append(abnormal_url(url))
    status.append(count_dot(url))
    status.append(count_www(url))
    status.append(count_atrate(url))
    status.append(no_of_dir(url))
    status.append(no_of_embed(url))
    status.append(shortening_service(url))
    status.append(count_https(url))
    status.append(count_http(url))
    status.append(fd_length(url))
    tld = get_tld(url, fail_silently=True)
    status.append(tld_length(tld))
    return status

@app.route('/', methods=['GET', 'POST'])
def index():
    sms_result = None
    url_result = None

    if request.method == 'POST':
        if 'sms' in request.form:
            sms = request.form['sms']
            sms_prediction = sms_model.predict([sms])
            sms_result = 'Spam' if sms_prediction == 1 else 'Not Spam'
        elif 'url' in request.form:
            url = request.form['url']
            features = get_url_features(url)
            features = np.array(features).reshape((1, -1))
            url_prediction = url_model.predict(features)
            if int(url_prediction[0]) == 0:
                url_result = "SAFE"
            elif int(url_prediction[0]) == 1.0:
                url_result = "DEFACEMENT"
            elif int(url_prediction[0]) == 2.0:
                url_result = "PHISHING"
            elif int(url_prediction[0]) == 3.0:
                url_result = "MALWARE"

    return render_template('index.html', sms_result=sms_result, url_result=url_result)

if __name__ == '__main__':
    app.run(debug=True)