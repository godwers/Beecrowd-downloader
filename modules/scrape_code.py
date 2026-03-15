from selenium.webdriver.common.by import By

from time import sleep


def _get_question_name(driver) -> str | None:
    return driver.title.split("-")[1]


def _click_edit_button(driver) -> None:
    driver.find_element(By.CLASS_NAME, "profile-buttons").click()


def _get_question_diffculty(driver) -> str | None:
    return driver.find_element(
        By.CSS_SELECTOR,
        "#page-name-c > ul:nth-child(2) > li:nth-child(3) > strong:nth-child(1)",
    ).text


def _get_category_problem(driver) -> str:
    return driver.find_element(
        By.CSS_SELECTOR, "#page-name-c > ul:nth-child(2) > li:nth-child(1)"
    ).text


def _get_code(driver) -> str:
    code = ""
    sleep(1)
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


def go_to_page_with_code(driver, unique_identifier: str) -> None:
    driver.get(f"https://judge.beecrowd.com/pt/runs/code/{unique_identifier}")


def get_question_information(driver, question_id: str = ""):
    code = _get_code(driver)
    _click_edit_button(driver)
    category_type = _get_category_problem(driver)
    code_title = f"Questão {question_id} - {_get_question_name(driver)} - {_get_question_diffculty(driver)}"
    return code, category_type, code_title
