import configparser

class Settings:
    """
    Object for defining fractal settings
    """
    def __init__(self, inipath):
        self.config = configparser.ConfigParser()
        self.config.read(inipath)

    def getitem(self, section, setting, converter):
        """
        Return value from ini file converted with converter function.
        converter:
        int for integers
        str for strings
        etc.
        :param section: Section name
        :param setting: Setting name
        :param converter: Type conversion function to use
        :return: value converted with converter function
        """
        return converter(self.config[section][setting])

    def getlist(self, section, setting, converter):
        settingstring = self.getitem(section, setting, str)
        return [converter(value) for value in settingstring.split(';')]

    def getlist2d(self, section, setting, converter):
        sublists = self.getlist(section, setting, str)
        return [[converter(value) for value in sublist.split(',')] for sublist in sublists]