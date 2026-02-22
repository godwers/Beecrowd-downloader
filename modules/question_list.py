from time import sleep
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import (
    ElementNotInteractableException,
    NoSuchElementException,
    ElementClickInterceptedException,
)
from .constants import ACCEPTED_LIST_URL


def _get_lastpage(driver, xpath: str) -> str | None:
    try:
        last_page = (
            WebDriverWait(driver, 15)
            .until(EC.presence_of_element_located((By.XPATH, xpath)))
            .get_attribute("href")
        )

        if not last_page:
            print("Something gone wrong")
            return ""

        return last_page
    except ElementNotInteractableException:
        _get_lastpage(driver, xpath)


def _get_page_number(driver) -> int | None:
    try:
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        sleep(5)
        link_to_last_page = _get_lastpage(
            driver, "/html/body/div/div/div[2]/div[4]/div/div[2]/div[2]/li[4]/a"
        )

        if not link_to_last_page:
            return 1

        last_page = link_to_last_page.split("=")[2]

        return int(last_page)
    except ElementNotInteractableException or ElementClickInterceptedException:
        _get_page_number(driver)


def _list_loop(driver) -> dict:
    questions_list = dict()
    pagina_final = _get_page_number(driver)

    if not pagina_final:  # fuck pyright
        pagina_final = 1

    pagina = 1
    while pagina <= pagina_final:
        driver.get(f"{ACCEPTED_LIST_URL}&page={pagina}&sort=problem_id&direction=asc")
        # driver.execute_script("document.body.style.zoom = '0.5'")
        sleep(5)
        try:
            for i in range(1, 29):
                numeros = int(
                    driver.find_element(
                        By.XPATH,
                        f"/html/body/div/div/div[2]/div[4]/div/div[2]/table/tbody/tr[{i}]/td[3]/a",
                    ).text
                )
                linguagem = driver.find_element(
                    By.XPATH,
                    f"/html/body/div[7]/div/div[2]/div[4]/div/div[2]/table/tbody/tr[{i}]/td[6]",
                ).text

                if linguagem not in questions_list:
                    questions_list[linguagem] = set()

                questions_list[linguagem].add(numeros)
            pagina += 1
            sleep(1)

        except NoSuchElementException:
            if pagina + 1 > pagina_final:
                break
            continue
    return questions_list


def get_solved_list(driver) -> dict:
    driver.get(ACCEPTED_LIST_URL)
    question_list = _list_loop(driver)

    for i in question_list:
        lista_questoes = list(question_list[i])
        lista_questoes.sort()
        question_list[i] = lista_questoes
    return question_list
