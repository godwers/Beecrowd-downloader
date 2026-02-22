from os import getcwd,remove

from wget import download

from .constants import UBLOCK_ORIGIN_URL

def _get_ublock_addon() -> str:
    return download(UBLOCK_ORIGIN_URL,bar=None,out=getcwd())

def add_ublock(driver):
    path_file = _get_ublock_addon()
    driver.install_addon(path_file)
    return path_file

def remove_ublock(path_file):
    remove(path_file)
