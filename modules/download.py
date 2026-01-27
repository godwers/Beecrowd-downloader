from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait
from selenium.common.exceptions import NoSuchElementException, TimeoutException

from time import sleep

from .constants import LANGUAGE_ID


def get_question_name(driver) -> str | None:
    return driver.title.split("-")[1]


def click_edit_button(driver) -> None:
    sleep(2)
    driver.find_element(By.XPATH, "/html/body/div[7]/div/div[2]/div[1]/div/a").click()
    sleep(2)


def get_question_diffculty(driver) -> str | None:
    return driver.find_element(
        By.XPATH, "/html/body/div[8]/div[2]/div[1]/div/ul/li[3]/strong"
    ).text


def get_category_problem(driver) -> str | None:
    try:
        click_edit_button(driver)
        return (
            WebDriverWait(driver, 30)
            .until(
                EC.presence_of_element_located(
                    (By.XPATH, "/html/body/div[8]/div/div[1]/div/ul/li[1]")
                )
            )
            .text
        )
    except TimeoutException:
        get_category_problem(driver)


def get_code(driver) -> str:
    code = ""
    code_range: range = range(
        len(
            driver.execute_script(
                "return document.getElementsByClassName('ace_line');"  # this script should return a list
            )
        )
    )
    for _ in code_range:
        code += (
            driver.execute_script(
                f"return document.getElementsByClassName('ace_line')[{_}].textContent;"
            )
            + "\n"
        )

    return code


def get_question_information(driver, question_id: int = -1):
    code = get_code(driver)
    category_type = get_category_problem(driver)
    code_title = f"Questão {question_id} - {get_question_name(driver)} - {get_question_diffculty(driver)}"
    return code, category_type, code_title


def go_to_page_with_code(
    driver, question_id: int = -1, language: str = "x86_64"
) -> None:
    while True:
        try:
            answer_url = f"https://judge.beecrowd.com/pt/runs?problem_id={question_id}&answer_id=1&language_id={LANGUAGE_ID[language]}"
            driver.get(answer_url)
            sleep(2)
            code_id = driver.find_element(By.CLASS_NAME, "id").text
            driver.get(f"https://judge.beecrowd.com/pt/runs/code/{code_id}")
            break
        except NoSuchElementException:
            continue
