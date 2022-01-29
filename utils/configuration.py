import configparser


class ConfigParser:
    config_path = '/Users/ivan.shkurko/test_repo/config.cfg'
    config_parser = configparser.RawConfigParser(allow_no_value=True)
    with open(config_path) as configFile:
        config_parser.read_file(configFile)
    config_parser.sections()

    @staticmethod
    def get_config(path):
        config = configparser.RawConfigParser(allow_no_value=True)
        with open(path) as configFile:
            config.read_file(configFile)
        config.sections()
        return config
