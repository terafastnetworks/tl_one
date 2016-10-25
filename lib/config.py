import os
import ConfigParser
Config = ConfigParser.ConfigParser()
Config.read('config.txt')

## get switch login credinals
def get_config_arg(opr, argName):
    try:
        Name = Config.get(opr, argName)
        return Name
    except Exception as err:
        return err
