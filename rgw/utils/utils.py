import os
import hashlib
import subprocess
import log
import json
import glob


def get_md5(file_path):

    return hashlib.md5(open(file_path, 'rb').read()).hexdigest()


def create_file(fname, size):

    # give the size in mega bytes.

    file_size = 1024 * 1024 * size

    with open(fname, 'wb') as f:
        f.truncate(file_size)

    fname_with_path = os.path.abspath(fname)

    md5 = get_md5(fname)

    return fname_with_path, md5


def split_file(fname, size_to_split=5):

    try:

        split_cmd = "split" + " " + '-b' + str(size_to_split) + "m " + fname
        subprocess.check_output(split_cmd, shell=True, stderr=subprocess.STDOUT)

    except subprocess.CalledProcessError as e:
        error = e.output + str(e.returncode)
        log.error(error)
        return False


class JsonOps(object):

    def __init__(self, fname):
        self.fname = fname
        self.mp_id = None
        self.key_name = None
        self.total_parts_count = 0
        self.remaining_file_parts = []

    def create_json_data(self):

        log.info('creating json data')

        json_data = {'mp_id' : self.mp_id,
                     'key_name' : self.key_name,
                     'total_parts': self.total_parts_count,
                     'remaining_parts': self.remaining_file_parts
                     }

        return json_data

    def create_update_json_file(self):

        log.debug('creating_updating json file')

        json_data = self.create_json_data()

        with open(self.fname, "w") as fp:
            json.dump(json_data, fp, indent=4)

    def refresh_json_data(self):

        log.info('loading / refreshing json file')

        with open(self.fname) as fp:
            json_data = json.load(fp)

        self.total_parts_count = json_data['total_parts']
        self.remaining_file_parts = json_data['remaining_parts']
        self.key_name = json_data['key_name']
        self.mp_id = json_data['mp_id']


def break_connection():
    pass
