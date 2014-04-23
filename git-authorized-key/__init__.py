import authkey
import pygit2
import shutil
import sys
from datetime import timedelta,datetime
from glob import iglob

## do the config parser import based on python version
if sys.version_info[0] == 2:
    import ConfigParser as configparser
else:
    import configparser

_FAILURE = 1
_DEFAULT_TTL = 1440 # 1 day in minutes
_CONFIG_SECT = 'GLOBAL'
_CONFIG_FILENAME = 'git-authorized-keys.conf'
_CONFIG_DEFAULTS = { 'ttl' : _DEFAULT_TTL }

def _check_version():
    """Function to check that we're on python 2.6 or greater"""
    req_version = (2,6)
    if sys.version_info < req_version:
        sys.exit("ERROR: Must be on python 2.6 or greater\n")

def _get_repo_info(configobj,sect=_CONFIG_SECT):
    repo_url = configobj.get(sect,'repo_url')
    check_loc = configobj.get(sect,'checkout_directory')
    check_loc = os.path.expandvars(check_loc)
    ttl = configobj.getint(sect,'checkout_ttl')
    ttl = datetime.timedelta(minutes=ttl)
    return (repo_url,check_loc,ttl)

def _get_config_file():
    dirs_to_check = ['/etc','/usr/local/etc']
    for dirname in dirs_to_check:
        configfile = os.path.join(dirname,_CONFIG_FILENAME)
        if os.path.exists(configfile):
            return configfile

    ## if we get here we obviously didn't find a config file
    sys.exit("ERROR: No configuration file found\n")

def _check_expired(path,ttl):
    now = datetime.now()
    mtime = os.path.getmtime(path)
    mtime = datetime.fromtimestamp(mtime)
    difference = now - mtime
    if difference >= ttl:
        return True
    else:
        return False

def _clone_repo(url,path,ttl):
    if os.path.exists(path):
        ## blow away the repo if the TTL expired
        ## so we can clone it again
        if _check_expired(path,ttl):
            shutil.rmtree(path)
        else:
            repo = pygit2.Repository(path)
    else:
        repo = pygit2.clone_repository(url,path)

    return repo

def main():
    username = sys.argv[1]
    configfile = _get_config_file()
    config = configparser.ConfigParser(_CONFIG_DEFAULTS)
    with open(configfile) as fh_config:
        config.readfp(fh_config)

    checkout_url,checkout_path,ttl = _get_repo_info(config)
    repo = _clone_repo(checkout_url,checkout_path,ttl)
    key_filepattern = os.path.join(repo.path,username,'*.pub')
    for pubkey_file in glob.iglob(key_filepattern):
        with open(pubkey_file) as fh_pubkey:
            key_str = fh_pubkey.read()
        key = authkey.create_authorized_key(key_str)
        print(key)

