from time import sleep

from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException

from .constants import ACCEPTED_LIST_URL


def _get_lastpage(driver, xpath: str) -> str | None:
        last_page = driver.find_element(By.XPATH,xpath).get_attribute("href")
        if not last_page:
            print("Something gone wrong")
            return ""

        return last_page


def _get_page_number(driver) -> int | None:
        link_to_last_page = _get_lastpage(
            driver, "/html/body/div/div/div[2]/div[4]/div/div[2]/div[2]/li[4]/a"
        )

        if not link_to_last_page:
            return 1

        last_page = link_to_last_page.split("=")[2]

        return int(last_page)


def _list_loop(driver) -> dict[str,list[dict[str,str]]]:
    questions_list = dict()
    pagina_final = _get_page_number(driver)

    if not pagina_final:  # fuck pyright
        pagina_final = 1

    pagina = 1
    while pagina <= pagina_final:
        driver.get(f"{ACCEPTED_LIST_URL}&page={pagina}&sort=problem_id&direction=asc")
        sleep(5)
        try:
            for i in range(1, 29):
                codigo_unico = driver.find_element(
                        By.XPATH, 
                        f"/html/body/div[7]/div[2]/div[2]/div[4]/div/div[2]/table/tbody/tr[{i}]/td[1]"
                ).text
                
                numeros = driver.find_element(
                        By.XPATH, 
                        f"/html/body/div/div/div[2]/div[4]/div/div[2]/table/tbody/tr[{i}]/td[3]/a"
                ).text
                
                linguagem = driver.find_element(
                    By.XPATH,
                    f"/html/body/div[7]/div/div[2]/div[4]/div/div[2]/table/tbody/tr[{i}]/td[6]",
                ).text

                if linguagem not in questions_list:
                    questions_list[linguagem] = list()

                unique_identifier = {numeros : codigo_unico}

                questions_list[linguagem].append(unique_identifier)
            pagina += 1
            sleep(1)

        except NoSuchElementException:
            if pagina + 1 > pagina_final:
                break
            continue

    return questions_list


def get_solved_list(driver) -> dict[str,list[dict[str,str]]]:
    driver.get(ACCEPTED_LIST_URL)
    question_list = _list_loop(driver)

    return question_list
