#!/usr/bin/python

import subprocess
import shutil
import os
import os.path
import json

import click

@click.group()
def cli():
    """A easy to use CLI interface to BitTorrentSync"""
    pass

def load_config():
    """Reads the (json) cli_btsync config file.

    Input:
        None
    Output:
        Config dictionary
    """
    base = os.path.dirname(__file__)
    with open(os.path.join(base, "cli_btsync.config"), "r") as cf:
        return json.loads(cf.read())

def dump_config(config):
    """Dumps the cli_btsync config dictionary to
        cli_btsync config file (json)
        btsync config file (btsync format)
    
    Input: 
        Config dictionary
    Output:
        None
    """
    base = os.path.dirname(__file__)
    with open(os.path.join(base, "cli_btsync.config"), "w") as cf:
        cf.write(json.dumps(config))
    with open(os.path.join(base, "btsync.config"), "w") as cf:
        cf.write(json.dumps(convert_config(config)))
 
def convert_config(config):
    """Converts cli_btsync config into a btsync config"""
    btsync_config = {
        "device_name": config["device_name"],
        "listening_port": 0,
        "use_upnp": True,
        "download_limit": 0,
        "upload_limit": 0,
        "shared_folders": [
            {
                "secret": sf["secret"],
                "dir": sf["dir"],
                "use_tracker": True,
                "use_dht": False,
                "search_lan": True,
                "use_sync_trash": True,
                "overwrite_changes": False,
                "known_hosts": []
            }
            for sf in config["shared_folders"] 
        ]
    }
    return btsync_config

@click.command()
@click.option(
    "--btsync_path",
    prompt="Give the path to the btsync executable",
    help="Path to the btsync executable",
    type=click.Path(exists=True)
)
@click.option(
    "--device_name",
    prompt="Give a name for your new device",
    help="Name for your new device"
)  
def bootstrap(btsync_path, device_name):
    """Initialises the cli_btsync application"""
    
    config = {
        "btsync_path": btsync_path,
        "device_name": device_name,
        "shared_folders": [],
    }

    dump_config(config)
cli.add_command(bootstrap)


@click.command()
@click.option(
    "--show_secrets/--hide_secrets",
    help="Adds the secret keys to the output of ls",
    default=False
)
def ls(show_secrets):
    """List all shared folders"""
    cfg = load_config()
    print("All shared folders for device {}:".format(cfg["device_name"]))
    
    if len(cfg["shared_folders"]) == 0:
        print("\t No shared folders")
    else:
        for sf in cfg["shared_folders"]:
            if show_secrets:
                print("\t{}\t{}".format(sf["dir"], sf["secret"]))
            else:
                print("\t{}".format(sf["dir"]))
cli.add_command(ls)   

@click.command()
@click.option(
    "--folder",
    prompt="What folder?",
    help="The folder that needs to be shared",
    type=click.Path(exists=True)
)
@click.option(
    "--secret",
    help="the secret (if empty a secret will be generated)"
)
def add(folder, secret):
    """Add a folder to be shared"""
    cfg = load_config()
    if not secret:
        secret = subprocess.check_output([
            cfg["btsync_path"],
            "--generate-secret"
        ]).strip()
    
    cfg["shared_folders"].append({
        "dir": folder,
        "secret": secret
    })

    dump_config(cfg)
    print("Added {} to the shared folders".format(folder))
cli.add_command(add)

@click.command()
@click.option(
    "--folder",
    prompt="What folder?",
    help="The shared folder that will be removed",
    type=click.Path()
)
@click.option(
    "--remove_archive/--keep_archive",
    help="Remove the btsync archive as well",
    default=False
)
def rm(folder, remove_archive):
    """Remove a shared folder from syncing"""
    cfg = load_config()
    new_shared_folders = []
    for sf in cfg["shared_folders"]:
        if not sf["dir"] == folder:
            new_shared_folders.append(sf)
        else:
            print("{} has been removed".format(folder))
    cfg["shared_folders"] = new_shared_folders
    dump_config(cfg)

    archive = os.path.join(folder, ".sync")
    if os.path.exists(archive) and remove_archive:
        shutil.rmtree(archive)
        print("Removed archive")
cli.add_command(rm)

@click.command()
def start():
    """Start syncing"""
    cfg = load_config()
    base = os.path.dirname(__file__)
    subprocess.call(
        "{} --config {}".format(
            cfg["btsync_path"],
            os.path.join(base, "btsync.config")
        ),
        shell=True
    )
cli.add_command(start)

if __name__ == "__main__":
    cli()
