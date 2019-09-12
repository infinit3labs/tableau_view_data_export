import requests
import json

import tableau_api.pub_tableau_api_urls as ta_urls
import tableau_api.pvt_tableau_api_admin as ta_admin

# Error Codes 200-209


def auth(server, site):
    server_name = server
    user_name = []
    password = []
    # Not published to repo
    if ta_admin.admin_creds:
        user_name.append(ta_admin.admin_creds['username'])
        # Not published to repo
        password.append(ta_admin.admin_creds['password'])
    else:
        # ERROR CODE 200: Either admin module missing, or credentials invalid.
        print('Server credentials invalid.\n'
              'Contact support for assistance. [Error Code 200]')
        exit(200)
    site_url_id = site

    signin_url = ta_urls.urls['sign-in'].format(server=server_name)

    payload = {
        'credentials': {
            'name': user_name[0],
            'password': password[0],
            'site': {
                'contentUrl': site_url_id
            }
        }
    }

    headers = {
        'accept': 'application/json',
        'content-type': 'application/json'
    }
    try:
        req = requests.post(signin_url, json=payload, headers=headers)
        req.raise_for_status()
        response = json.loads(req.content)
        token = response['credentials']['token']
        site_id = response['credentials']['site']['id']
        print('Sign in successful!')
        headers['X-tableau-auth'] = token

        return {
            'headers': headers,
            'site_id': site_id
        }
    except requests.ConnectionError:
        # ERROR CODE 201: User entered a domain and client ID combination that failed.
        print('Connection failed using:\n'
              '* Server Domain = \'{}\'\n'
              '* Client ID = \'{}\'\n'
              'Please contact support for assistance. [Error Code 201]'.format(server,
                                                                               site_url_id))
        exit(201)
