from selenium import webdriver

from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.by import By

from time import sleep

from modules.login import login
from modules.question_list import get_solved_list
from modules.repository import create_repository
from modules.constants import LANGUAGE_ID
from modules.download import get_question_information


def main() -> None:
    options = webdriver.FirefoxOptions()
    options.add_argument("--headless=new")  # Comment this line to debug
    driver = webdriver.Firefox(options=options)

    login(driver)

    print("Login Successfully")

    solved_list = get_solved_list(driver)
    print("Accepted answers was retrived")
    print(solved_list)

    create_repository()

    for language in solved_list:
        pointer = 0
        questions_list = solved_list[language]
        while pointer < len(questions_list):
            try:
                sleep(1)
                answer_url = f"https://judge.beecrowd.com/pt/runs?problem_id={questions_list[pointer]}&answer_id=1&language_id={LANGUAGE_ID[language]}"
                driver.get(answer_url)
                resolucao_id = driver.find_element(By.CLASS_NAME, "id").text
                driver.get(f"https://judge.beecrowd.com/pt/runs/code/{resolucao_id}")
                sleep(2)
                driver.find_element(
                    By.XPATH, "/html/body/div[7]/div/div[2]/div[1]/div/a"
                ).click()
                sleep(2)

                code, category_type, code_title = get_question_information(
                    driver, question_id=questions_list[pointer]
                )
                print(code_title)
                print(category_type)
                print(code)

                pointer += 1
                sleep(1)
            except TimeoutException:
                continue
    driver.close()


if __name__ == "__main__":
    main()
