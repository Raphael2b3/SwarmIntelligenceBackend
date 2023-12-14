import os

import os.path
import dotenv

loaded = False


def warn_if_env_not_loaded(func):
    def wrapper(*args, **kwargs):
        if not loaded:
            print("WARNING: Environment not loaded, call load_env.load() before calling.")
        return func(*args, **kwargs)

    return wrapper


def load(path=".env"):
    global loaded
    print("loading ENVIRONMENT variables")
    if os.path.exists(path):
        dotenv.load_dotenv(path)
        loaded = True
    else:
        message = """Read the README.md and create a .env file. 
        copy the .env.example and define the parameters in it """

        raise Exception(message)


@warn_if_env_not_loaded
def load_settings_from_env_dict(*key_list):
    env = {}

    for key in key_list:
        value = os.getenv(key)
        if value is None:
            raise Exception(key + " is not set in environment, check your .env file")
        env[key] = value
    return env


@warn_if_env_not_loaded
def load_settings_from_env(*key_list):
    for key in key_list:
        value = os.getenv(key)
        if value is None:
            raise Exception(key + " is not set in environment, check your .env file")
        yield value


load()
