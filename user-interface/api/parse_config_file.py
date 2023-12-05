import configparser


def _parse_config(filename: str) -> configparser.ConfigParser:
    """
    Parses a config file containing application-level settings.
    :param filename: The name of the config file.
    :return: The config settings.
    """
    config = configparser.ConfigParser()
    config.read(filename)
    return config


config = _parse_config("settings.ini")
