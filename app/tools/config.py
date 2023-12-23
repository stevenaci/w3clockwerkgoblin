
from configparser import ConfigParser
from tools.singleton import Singleton

class ConfigSection:
    def __init__(self, section: str, kvals: dict):
        self.section, self.kvals = section, kvals

credential_section = ConfigSection(
    'credential',
    {
        'access_token':'',
        'refresh_token':'',
        'client_id':'',
        'client_secret':'',
        'testing':'True'
        }
    )

class Config(ConfigParser, Singleton):

    def __init__(self, config_file: str, required_sections: list[ConfigSection]):
        super().__init__()
        self.config_file = config_file
        self.read(config_file)
        self.create_required_sections(required_sections)

    def create_required_sections(self, required_sections: list[ConfigSection]):
        """ 
            Check if the required sections/keys exist, saves them to the current self.configfile.
            
            If the keys don't exist, they will be initialized with their placeholders
        """
        needs_save = False
        for required_section in required_sections:
            if not self.has_section(required_section.section):
                needs_save = True
                self.add_section(required_section.section)

            # If the keys don't exist, add them
            for key in required_section.kvals.keys():
                if not self.has_option(required_section.section, key):
                    needs_save = True
                    self.set(required_section.section, key, required_section.kvals[key])

        if needs_save:
            with open(self.config_file, 'w+') as configfile:
                print(f'Creating required config file, please update before continuing: {configfile.name}')
                self.write(configfile)
                exit()

config = Config(
    'twitch.ini', [credential_section]
)