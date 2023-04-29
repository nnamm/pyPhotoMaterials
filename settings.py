"""settings.py"""

import configparser

from utils import bool_from_str

conf = configparser.ConfigParser()
conf.read("settings.ini")

photo_work_dir = conf["dir"]["photo"]
text_work_dir = conf["dir"]["text"]

s_size = conf["size"]["size_1"]
m_size = conf["size"]["size_2"]
l_size = conf["size"]["size_3"]
image_sizes = [s_size, m_size, l_size]

ftps_host = conf["ftps"]["server"]
ftps_user = conf["ftps"]["user"]
ftps_passwd = conf["ftps"]["passwd"]
ftps_product_path = conf["ftps"]["product_path"]
ftps_test_path = conf["ftps"]["test_path"]
ftps_test_flag = bool_from_str(conf["ftps"]["test_env_flag"])
ftps_home_url = conf["ftps"]["home"]

bitly_api_url = conf["bitly"]["api"]
bitly_domain = conf["bitly"]["domain"]
bitly_access_token = conf["bitly"]["token"]
