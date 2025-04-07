# import os
# import configparser


# class Manager:
#     """
#     A configuration management class for handling environment-specific settings.

#     This class provides functionality to load, create, and manage configuration variables 
#     from an INI file. It allows dynamic configuration of environment variables, with the 
#     ability to reset or recreate the configuration as needed.

#     Attributes:
#         file (str): Path to the configuration file (default is 'config.ini')
#         config_vars (dict): A dictionary to store configuration variables after loading

#     Key Methods:
#         load_vars(): Loads configuration variables from the INI file into environment variables
#         reset_config(): Removes the existing configuration file and creates a new template
#         __create_config_template(): Creates a default configuration file with predefined variables

#     Example:
#         >>> config_manager = Manager()
#         >>> config_manager.load_vars()
#         >>> # Access environment variables
#         >>> bucket_name = os.environ.get('BUCKET_NAME')
#     """

#     def __init__(self, config_path: str = 'config.ini'):

#         self.utils_dir = os.path.dirname(__file__)
#         self.file = os.path.join(self.utils_dir, config_path)
#         self.config_vars = {}

#     def load_vars(self):

#         if not os.path.isfile(self.file):
#             self.__create_config_template()

#         config = configparser.ConfigParser()
#         config.read(self.file)

#         self.__read_config_section(config, 'Settings')
#         self.__read_config_section(config, 'Scrapper Settings')

#         # Other custom Vars here - if any
#         os.environ['HOME_DIR'] = os.path.dirname(self.utils_dir)

#         # status set for scripts to verify
#         os.environ['ENV_STATUS'] = '1'

#     def reset_config(self):

#         print("Resetting Configuration")
#         os.remove(self.file)
#         self.config_vars = {}
#         self.__create_config_template()

#     def __read_config_section(self, config, section_name):

#         for key, value in config[section_name].items():
#             value = value.strip("'\"")

#             # Set environment variable
#             os.environ[key.upper()] = value
#             self.config_vars[key.upper()] = value

#     def __create_config_template(self):

#         config = configparser.ConfigParser()

#         config['Settings'] = {
#             'rawdata_dir': '/Users/sudarshanp/Desktop/UniQbot-rag/data/scraped_pages',
#             'cleandata_dir': '/Users/sudarshanp/Desktop/UniQbot-rag/data/cleaned_html',
#             'chunkdata_dir': '/Users/sudarshanp/Desktop/UniQbot-rag/data/chunks',
#             'anthropic_model': "claude-3-haiku-20240307",
#             'anthropic_api_key': '',
#             'openai_model': 'gpt-3.5-turbo',
#             'openai_api_key': '',
#         }
#         config['Scrapper Settings'] = {
#             'sitemap': 'https://international.northeastern.edu/ogs',
#             'workers': '30',
#             'env_status': '0',
#         }

#         with open(self.file, 'w+') as configfile:
#             config.write(configfile)

#         print(f"Configuration file created")

import os
import configparser


class Manager:
    """
    A configuration management class for handling environment-specific settings.

    This class provides functionality to load, create, and manage configuration variables 
    from an INI file. It allows dynamic configuration of environment variables, with the 
    ability to reset or recreate the configuration as needed.

    Attributes:
        file (str): Path to the configuration file (default is 'config.ini')
        config_vars (dict): A dictionary to store configuration variables after loading
        selected_model (str): Currently selected model (claude or gpt)

    Key Methods:
        load_vars(): Loads configuration variables from the INI file into environment variables
        reset_config(): Removes the existing configuration file and creates a new template
        set_model(): Sets the currently selected model
        __create_config_template(): Creates a default configuration file with predefined variables

    Example:
        >>> config_manager = Manager()
        >>> config_manager.load_vars()
        >>> # Access environment variables
        >>> bucket_name = os.environ.get('BUCKET_NAME')
    """

    def __init__(self, config_path: str = 'config.ini'):
        self.utils_dir = os.path.dirname(__file__)
        self.file = os.path.join(self.utils_dir, config_path)
        self.config_vars = {}
        self.selected_model = "claude"  # Default model

    def load_vars(self):
        if not os.path.isfile(self.file):
            self.__create_config_template()

        config = configparser.ConfigParser()
        config.read(self.file)

        self.__read_config_section(config, 'Settings')
        self.__read_config_section(config, 'Scrapper Settings')

        # Other custom Vars here - if any
        os.environ['HOME_DIR'] = os.path.dirname(self.utils_dir)

        # status set for scripts to verify
        os.environ['ENV_STATUS'] = '1'

    def reset_config(self):
        print("Resetting Configuration")
        os.remove(self.file)
        self.config_vars = {}
        self.__create_config_template()

    def set_model(self, model_name):
        """Set the currently selected model (claude or gpt)"""
        if model_name in ["claude", "gpt"]:
            self.selected_model = model_name
            print(f"Model set to: {model_name}")
        else:
            print(f"Invalid model name: {model_name}. Using default (claude).")
            self.selected_model = "claude"

    def get_model(self):
        """Get the currently selected model"""
        return self.selected_model

    def __read_config_section(self, config, section_name):
        for key, value in config[section_name].items():
            value = value.strip("'\"")

            # Set environment variable
            os.environ[key.upper()] = value
            self.config_vars[key.upper()] = value

    def __create_config_template(self):
        config = configparser.ConfigParser()

        config['Settings'] = {
            'rawdata_dir': '/Users/sudarshanp/Desktop/UniQbot-rag/data/scraped_pages',
            'cleandata_dir': '/Users/sudarshanp/Desktop/UniQbot-rag/data/cleaned_html',
            'chunkdata_dir': '/Users/sudarshanp/Desktop/UniQbot-rag/data/chunks',
            'anthropic_model': "claude-3-haiku-20240307",
            'anthropic_api_key': '',
            'openai_model': 'gpt-3.5-turbo',
            'openai_api_key': '',
        }
        config['Scrapper Settings'] = {
            'sitemap': 'https://international.northeastern.edu/ogs',
            'workers': '30',
            'env_status': '0',
        }

        with open(self.file, 'w+') as configfile:
            config.write(configfile)

        print(f"Configuration file created")