import os 

from wget import download,filename_from_url

from .constants import UBLOCK_ORIGIN_URL


def _get_file_name() -> str:
    filename = filename_from_url(UBLOCK_ORIGIN_URL)
    return os.path.join(os.getcwd(),filename)

def _get_ublock_addon() -> None:
    download(UBLOCK_ORIGIN_URL,bar=None,out=os.getcwd())

def add_ublock(driver):
    path_file = _get_file_name()
    if not os.path.exists(path_file):
        _get_ublock_addon()
    driver.install_addon(path_file)
    return path_file

def remove_ublock(path_file):
    os.remove(path_file)
