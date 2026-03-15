from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait
from selenium.common.exceptions import (
    NoSuchElementException,
    TimeoutException,
    UnexpectedAlertPresentException,
)

from time import sleep

from .constants import LANGUAGE_ID


def _get_question_name(driver) -> str | None:
    return driver.title.split("-")[1]


def _click_edit_button(driver) -> None:
    sleep(3)
    driver.find_element(By.CLASS_NAME, "profile-buttons").click()
    sleep(2)


def _get_question_diffculty(driver) -> str | None:
    return driver.find_element(
        By.CSS_SELECTOR, "#page-name-c > ul:nth-child(2) > li:nth-child(3) > strong:nth-child(1)"
    ).text


def _get_category_problem(driver) -> str | None:
    try:
        return (
            WebDriverWait(driver, 30)
            .until(
                EC.presence_of_element_located(
                    (
                        By.CSS_SELECTOR,
                        "#page-name-c > ul:nth-child(2) > li:nth-child(1)",
                    )
                )
            )
            .text
        )
    except TimeoutException:
        _get_category_problem(driver)
    except UnexpectedAlertPresentException:
        driver.refresh()
        _get_category_problem(driver)


def _get_code(driver) -> str:
    code = ""
    sleep(2)
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


def go_to_page_with_code(
    driver, question_id: int = -1, language: str = "x86_64"
) -> None:
    while True:
        try:
            answer_url = f"https://judge.beecrowd.com/pt/runs?problem_id={question_id}&answer_id=1&language_id={LANGUAGE_ID[language]}"
            driver.get(answer_url)
            sleep(3)
            code_id = driver.find_element(By.CLASS_NAME, "id").text
            driver.get(f"https://judge.beecrowd.com/pt/runs/code/{code_id}")
            break
        except NoSuchElementException:
            continue


def get_question_information(driver, question_id: int = -1):
    code = _get_code(driver)
    _click_edit_button(driver)
    category_type = _get_category_problem(driver)
    code_title = f"Questão {question_id} - {_get_question_name(driver)} - {_get_question_diffculty(driver)}"
    return code, category_type, code_title
