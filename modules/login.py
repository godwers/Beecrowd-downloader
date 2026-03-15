from getpass import getpass
from time import sleep

from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys

from .constants import LOGIN_URL, HOME_URL


def _check_login(driver, url) -> bool:
    sleep(3)
    if driver.current_url == url:
        return True
    return False


def login(driver) -> None:
    driver.get(LOGIN_URL)
    sleep(2)
    driver.refresh() #thanks ublock

    username = input("Digite seu email: ")
    driver.find_element(By.NAME, "email").send_keys(username)
    password = getpass(prompt="Digite a senha da conta: ",echo_char="*")
    driver.find_element(By.NAME, "password").send_keys(password + Keys.ENTER)

    if not _check_login(driver, HOME_URL):
        print("Wrong email or password!")
        login(driver)
