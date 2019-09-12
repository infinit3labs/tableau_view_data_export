import requests
import json

import tableau_api.pub_tableau_api_urls as ta_urls

# Error Codes: 210-219
VERSION = 1.1


def get_views(server, site, headers):
    view_ids = {}
    views_url = ta_urls.urls['views'].format(server=server,
                                             site=site)
    req = requests.get(views_url, headers=headers)
    req.raise_for_status()
    response = json.loads(req.content)
    for view in response['views']['view']:
        view_ids[view['name']] = view['id']
    return view_ids
