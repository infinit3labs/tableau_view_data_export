import requests
import csv

import writer
import tableau_api.pub_tableau_api_urls as ta_urls

# Error Codes: 220-229


def get_data(server, site_data, view_data, headers, loc=None, env='local'):
    client_name = site_data[0]
    site_id = site_data[1]
    view_name = view_data[0]
    view_id = view_data[1]
    data_url = ta_urls.urls['data'].format(server=server,
                                           site=site_id,
                                           view=view_id)
    req = requests.get(data_url, headers=headers)
    req.raise_for_status()
    decoded_content = req.content.decode('utf-8')

    cr = csv.reader(decoded_content.splitlines(), delimiter=',')
    tmp_list = list(cr)
    writer.csv_writer(obj=tmp_list,
                      root_folder=client_name,
                      sub_folder='{view_name}'.format(view_name=view_name),
                      env=env)
    return None
