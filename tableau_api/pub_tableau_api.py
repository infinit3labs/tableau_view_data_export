import requests
import getpass

import tableau_api.pub_tableau_api_auth as ta_auth             # Error Codes: 200-209
import tableau_api.pub_tableau_api_get_views as ta_views        # Error Codes: 210-219
import tableau_api.pub_tableau_api_get_data as ta_data         # Error Codes: 220-229
import tableau_api.pub_tableau_api_urls as ta_urls
import tableau_api.pvt_tableau_api_client_creds as ta_creds
import tableau_api.pvt_tableau_api_admin as ta_admin

# Options: 'local' = run on personal computer; 'dw' run on DW server
ENVIRONMENT = 'dw'


def term_red(skk): print("\033[91m{}\033[00m".format(skk))


def get_view_name(views):
    cnt = 0
    while cnt < 6:
        # Function to allow for multiple user errors with view data entry.
        input_view = input('\nEnter report option to export data:\n'
                           '\t(use a label above as input)\n')
        if input_view in views:
            return input_view
        elif input_view not in views and cnt < 4:
            print('Try again')
            cnt += 1
            continue
        else:
            term_red('*** This is your last attempt.')
            cnt += 1
            continue


def main(env):
    # All data entry fields are lists to allow for future functionality to handle
    # mutiple values. Currently only single values accepted.
    input_server = []
    input_site = []
    headers = []
    site_id = []
    # Check Environment to display correct user input prompts
    if env == 'local':
        # Not published to repo
        print('Using: {}'.format(ta_admin.admin_data['server']))
        # Not published to repo
        input_server.append('{}'.format(ta_admin.admin_data['server']))
        _input_site = str(input('\nEnter client site name: '))
        input_site.append(_input_site)
    elif env == 'dw':
        input_user_email = []
        input_user_pwd = []
        _input_user_email = str(input('\nEnter your username: '))
        # Use getpass library to mask user input; raises warning in IDE but can ignore
        _input_user_pwd = getpass.getpass()
        # Client data not published to repo
        # Use format:
        # creds = {
        #     'admin@example.com': {
        #         'name': 'John Smith',
        #         'password': 'password1',
        #         'client': {
        #             'example_client': {
        #                 'access_level': 'administrator'
        #             }
        #         }
        #     }
        if _input_user_email not in ta_creds.creds.keys()\
                or _input_user_pwd != ta_creds.creds[_input_user_email]['password']:
            print('Sorry, try again.')
            _input_user_email = str(input('\nEnter your username: '))
            _input_user_pwd = getpass.getpass()
            if _input_user_email not in ta_creds.creds.keys() \
                    or _input_user_pwd != ta_creds.creds[_input_user_email]['password']:
                # ERROR CODE 101: User has entered incorrect credentials twice.
                print('Sorry, the credentials are not valid.\n'
                      'Please contact support for assistance. [Error Code 101]')
                exit(101)
            else:
                input_user_pwd.append(_input_user_pwd)
                input_user_email.append(_input_user_email)
        else:
            input_user_pwd.append(_input_user_pwd)
            input_user_email.append(_input_user_email)
        if _input_user_email in ta_creds.creds.keys()\
                and input_user_pwd[0]:
            # Not published to repo
            input_server.append('{}'.format(ta_admin.admin_data['server']))
            _input_site = str(input('\nEnter client site ID: ') or '')
            if _input_site in ta_creds.creds[input_user_email[0]]['client'].keys():
                input_site.append(_input_site)
            elif _input_site == '':
                print('Please enter a client ID.')
                _input_site = str(input('\nEnter client site ID: ') or '')
                if _input_site in ta_creds.creds[input_user_email[0]]['client'].keys():
                    input_site.append(_input_site)
                elif _input_site == '':
                    # ERROR CODE 102: User entered a blank Client ID twice.
                    print('Please contact support for assistance. [Error Code 102]')
                    exit(102)
                else:
                    # ERROR CODE 900: Unhandled exception
                    print('Unhandled error with {}\n'
                          '[Error Code 900]'.format(_input_site))
                    exit(900)
            else:
                # ERROR CODE 103: Client ID entered does not exist or is not within user permissions.
                print('The client ID is not valid.\n'
                      'Please contact support. [Error Code 103]')
                exit(103)
        else:
            # ERROR CODE 104: User did not enter an email address on file.
            print('Sorry, the login has failed. Contact support for assistance. [Error Code 104]')
            exit(104)
    else:
        print('Unhandled environment: {} [Error Code 901]'.format(env))
        exit(901)

    #
    # START AUTH, HEADERS, SITE_ID BLOCK
    #

    if input_server[0] != '' \
            and input_site[0] != ''\
            and len(input_server) == 1\
            and len(input_site) == 1:
        _site_data = ta_auth.auth(server=input_server[0],
                                  site=input_site[0])
        headers.append(_site_data['headers'])
        site_id.append(_site_data['site_id'])
    else:
        exit('Please provide a single valid site URL and client ID.')

    #
    # END AUTH, HEADERS, SITE_ID BLOCK
    #

    #
    # GET VIEWS FOR CLIENT TO DISPLAY
    #

    views = ta_views.get_views(server=input_server[0],
                               site=site_id[0],
                               headers=headers[0])
    print('\nView Options:')
    for view_name in views.keys():
        print(view_name)
    _input_view_option = [get_view_name(views.keys())]

    #
    # GET SELECTED VIEW DATA
    #

    if _input_view_option[0] in views.keys()\
            and len(_input_view_option) == 1:
        ta_data.get_data(server=input_server[0],
                         site_data=(input_site[0], site_id[0]),
                         view_data=(_input_view_option[0], views[_input_view_option[0]]),
                         headers=headers[0],
                         env=ENVIRONMENT)
    else:
        # ERROR CODE 105: The user has entered 5 incorrect view options in a row.
        print('Too many invalid view options entered.\n'
              'Please contact support for assistance [Error Code 105]')
        exit(105)
    print('Export of \'{}\' Successful'.format(_input_view_option[0]))

    #
    # SIGN OUT
    #

    signout_url = ta_urls.urls['sign-out'].format(server=input_server[0])
    req = requests.post(signout_url, data=b'', headers=headers[0])
    req.raise_for_status()
    print('Sign out successful!')


if __name__ == '__main__':
    # Error Codes: 100-199 from main()
    main(ENVIRONMENT)
