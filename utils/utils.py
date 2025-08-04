from yaml import load, FullLoader


def load_config():

    with open("config.yaml", "r") as config_file:
        yaml_file = load(config_file, Loader=FullLoader)

        return yaml_file