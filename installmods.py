"""
FILE: installMods.py
AUTHOR: Zach Barnes
DATE: 5/17/22

Python script to install a list of dayz mods.

"""


from re import sub
import subprocess
import shutil
import os


STEAMCMD_PATH = r"C:\steamcmd\steamcmd"                 # path to steamcmd
SERVER_PATH = r"C:\dayzserver"                          # path to folder containing dayz server
DL_FOLDER = r"\steamapps\workshop\content\221100"       # path to mod download location from SERVER_PATH
KEY_MOD = r"\Keys\*.bikey"                              # path to mod key relative to mod folder
SERVER_KEYS = SERVER_PATH + r"\keys" + os.sep           # path to folder containing all server keys
DAYZ_ID = "221100"                                      # steam code for dayz
MODS = {                                                # dict of desired mods
    '1797720064' : '@WindstridesClothingPack',
    '1559212036' : '@CF'
}       


def installMod( id, name ):
    '''
    This function will be used to install a single mod, takes mod id and name as args.

    Precondition:
        The proper paths to steamcmd (STEAMCMD_PATH) 
        and server location (SERVER_PATH) must be set.

    Postcondition:
        The mod will be downloaded and moved into the 
        dayz server base folder. The mod key will also
        be copied into the keys folder.

    Args:
        id = mod id
        name = mod name
    '''
    # run steamcmd passing required arguements to download and validate the desired mod by id
    subprocess.run([ STEAMCMD_PATH, "+force_install_dir", SERVER_PATH, "+login", "anonymous",  
                     "+workshop_download_item", DAYZ_ID, id, "validate", "+quit" ])

    # set variables for old and new mod paths
    src_dir = SERVER_PATH + DL_FOLDER + os.sep + id     # moving mod from
    dest_dir = SERVER_PATH + os.sep + name              # moving mod into

    # here we perform the operation to remove any already existing modfolder in base server
    try:
        shutil.rmtree( dest_dir )
    except FileNotFoundError as error:
        print("Error deleting file: %s : %s :" % ( dest_dir, error.strerror ) )
    
    # here we attempt to move the mod into the base folder
    try:
        shutil.move( src_dir , dest_dir )
        src_dir = dest_dir + KEY_MOD
        command = "copy /y %s %s" % (src_dir, SERVER_KEYS)
        subprocess.run( command, shell = True )
    except FileNotFoundError as error:
        print("Error moving/copying file: %s : %s :" % ( src_dir, error.strerror ) )
    print("Successfully installed %s mod with id %s" % (name, id))


def main():
    for id in MODS:
        installMod( id, MODS[id] )


if __name__ == "__main__":
    main()