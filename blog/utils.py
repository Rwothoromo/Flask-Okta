from os.path import dirname, realpath


def get_app_base_path():
    return dirname(realpath(__file__))
