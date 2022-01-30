import configparser


class ConfigParser:
    # Для запуска тестов через Pycharm в config_path необходимо использовать абсолютный путь
    config_path = 'config.cfg'
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
