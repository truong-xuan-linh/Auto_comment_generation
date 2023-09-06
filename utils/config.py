import yaml

class Config():
    def __init__(self, dir) -> None:
        """Init function for Config class

        Args:
            dir (String): path to config file
        """
        self.dir = dir
    
    def __get_config__(self):
        """get config

        Returns:
            yaml: Yaml config
        """
        return yaml.load((open(self.dir)), Loader=yaml.SafeLoader)