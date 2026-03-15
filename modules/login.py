from getpass import getpass
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from time import sleep
from .constants import LOGIN_URL, HOME_URL


def check_login(driver, url) -> bool:
    if driver.current_url == url:
        return True
    return False


def login(driver) -> None:
    driver.get(LOGIN_URL)

    username = input("Digite seu email: ")
    password = getpass(prompt="Digite a senha da conta: ")

    driver.find_element(By.NAME, "email").send_keys(username)
    driver.find_element(By.NAME, "password").send_keys(password + Keys.ENTER)

    sleep(5)
    if not check_login(driver, HOME_URL):
        print("Wrong email or password!")
        login(driver)
