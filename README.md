CLI btsync
================

This is a command line interface for Bittorrent Sync (btsync).
The main use for this packages is for usage with a remote ssh server, where the btsync gui cannot be used.

Quickstart:

 - Download the btsync executable from the official website
 - Install Click, a CLI library for python
```
pip install click
```
 - Clone this repository
 - The use cli_btsync.py as follows

```   
# Initialise by calling the bootstrap function, must be done once
python cli_btsync.py bootstrap --btsync_path /path/to/bsync --device_name My_personal_device
# Add a folder that you want to sync to another device
python cli_btsync.py add --folder /home/user/folder/to/share
# List all the synced folders
python cli_btsync.py ls
# List all the synced folders, including the secrets
python cli_btsync.py ls --show_secrets
# I've you've received a secret key from someone, add it to btsync by
python cli_btsync.py add --folder /home/user/other/folder --secret ABCDEFGHIJ
# Remove a folder by
python cli_btsync.py rm --folder /home/user/folder/to/delete
# If additionally, you want to remove the archive as well
python cli_btsync.py rm --folder /home/user/other_folder --remove_archive
# Finally, start syncing
python cli_btsync.py start
```

Remarks:
---------
 - cli_btsync uses the old secrets instead of the new keys/link system.
 - Once you use cli_btsync, you can no longer use the GUI.
 - If you've used the GUI before, delete the .sync directory which is located in the same folder as the btsync executable. You will need to add all the shared folders again.
 - Only tested on Ubuntu & Raspbian
