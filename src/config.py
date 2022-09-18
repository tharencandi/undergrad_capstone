import os
from yaml import safe_load




def field_validator(config, *mandated_fields):
    for f in mandated_fields:
        if f not in config:
            raise KeyError(f"Field {f} is compulsory.")


def load_config(config_path, *validators):
    if not os.path.exists(config_path) or not os.path.isfile(config_path):
        raise FileNotFoundError("Config file does not exists.")

    conf = {}
    with open(config_path, "r") as conf:
        conf =  safe_load(conf)
        for v in validators:
            v(conf)

    return conf

