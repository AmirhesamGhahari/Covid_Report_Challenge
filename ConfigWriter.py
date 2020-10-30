from configparser import ConfigParser

# Create config object and initiate its keyWord
config_object = ConfigParser()
config_object["Local_Address"] = {"ExcelFile": "/Users/ahesam.gh/opt/anaconda3/envs/Exiger_Project"}

# Write the config object in a local file
with open("config.ini", 'w') as conf:
    config_object.write(conf)



