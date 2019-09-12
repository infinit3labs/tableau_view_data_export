import pandas as pd
import datetime
import csv
import os

VERSION = 1.1


def csv_writer(obj, root_folder='Testing', sub_folder='Testing', file_name=None, env='local', header=None):
    """
    :param obj: must be an iterable
    :param root_folder: this is the client name if passed from Tableau script; else is 'Testing'
    :param sub_folder: this is the view name if passed from Tableau script; else is 'Testing'
    :param file_name: (optional) default is current datetime
    :param env: default is local; to specify a different file system
    :param header: (optional) to pass in header row
    :return: None
    """
    # define the name of the directory to be created
    path = []
    if env == 'local':
        path.append('{}/{}/{}'.format(root_folder, sub_folder, datetime.date.today()))
    elif env == 'dw':
        path.append('/tmp/{}/{}/{}'.format(root_folder, sub_folder, datetime.date.today()))
    try:
        if not os.path.exists(path[0]):
            os.makedirs(path[0])
            if env == 'local':
                print("Successfully created the directory {}".format(path[0]))
    except OSError:
        if env == 'local':
            print("Creation of the directory {} failed".format(path[0]))
        elif env == 'dw':
            # ERROR CODE: 201
            print("Could create a required directory. Please notify support [Error Code: 201]")
    else:
        if env == 'local':
            print("Directory {} exists.".format(path[0]))

    if 'DataFrame' in str(type(obj)):
        _file_name = []
        if file_name:
            _file_name.append(file_name)
        else:
            _file_name.append(datetime.datetime.now())
        df = pd.DataFrame(obj)
        df.to_csv(path_or_buf='{}/{}.csv'.format(path[0], _file_name[0]),
                  header=None,
                  index=None)
    else:
        _file_name = []
        if file_name:
            _file_name.append(file_name)
        else:
            _file_name.append(datetime.datetime.now())
        with open('{}/{}.csv'.format(path[0], _file_name[0]), 'w') as f:
            writer = csv.writer(f)
            if header:
                writer.writerow(header)
                for line in obj:
                    writer.writerow(line)
            else:
                for line in obj:
                    writer.writerow(line)
