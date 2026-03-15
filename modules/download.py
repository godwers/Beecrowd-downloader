from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait
from selenium.common.exceptions import TimeoutException


def get_question_name(driver):
    question_name = driver.title
    return question_name.split("-")[1]


def get_question_diffculty(driver):
    return driver.find_element(
        By.XPATH, "/html/body/div[8]/div[2]/div[1]/div/ul/li[3]/strong"
    ).text


def get_category_problem(driver):
    try:
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


def get_question_information(driver, question_id=-1):
    code = get_code(driver)
    category_type = get_category_problem(driver)
    code_title = f"Questão {question_id} - {get_question_name(driver)} - {get_question_diffculty(driver)}"
    return code, category_type, code_title
