import os

"""
    Open_Folder():
"""
def Open_Folder(input_folder = None, furniture_name = None):
    if furniture_name:
        os.startfile(str(input_folder))