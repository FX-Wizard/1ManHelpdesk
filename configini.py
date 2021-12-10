from configparser import ConfigParser

class INIHandler():
    def __init__(self, fileName):
        '''opens and parses .ini files and saves them out again'''
        self.fileName = fileName
        self.config = ConfigParser(dict_type=AttrDict)
        try:
            self.config.read(fileName)
        except:
            raise("error reading file")
        self.ini = self.config._sections


    def __dict__(self):
        return self.config
        self.save()


    def save(self):
        '''saves out .ini file'''
        with open(self.fileName, 'w') as f:
            self.config.write(f)

    def addSection(self, section):
        self.config.add_section(section)


class AttrDict(dict):
    '''converts .ini file into python dict'''
    def __init__(self, *args, **kwargs):
        super(AttrDict, self).__init__(*args, **kwargs)
        self.__dict__ = self