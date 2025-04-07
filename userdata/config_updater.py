import os
import re
import time
import yaml

def get_id_and_password(key):
    yaml_file_name = 'credential/web_passwords.yaml'
    if os.path.exists(yaml_file_name):
        with open(yaml_file_name, 'r') as file:
            credential_list = yaml.safe_load(file)
            return credential_list[key]
    # We should not reach here
    return []
    
