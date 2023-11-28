import os


def load_settings_from_env(*key_list):
    env = {}
    for key in key_list:
        value = os.getenv(key)
        if value is None:
            raise Exception(key + " is not set in environment")
        env[key] = value
    return env
