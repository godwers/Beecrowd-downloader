from selenium import webdriver
from selenium.common.exceptions import TimeoutException

from time import sleep

from modules.login import login
from modules.question_list import get_solved_list
from modules.repository import create_repository, add_question
from modules.download import get_question_information, go_to_page_with_code


def main() -> None:
    options = webdriver.FirefoxOptions()
    options.add_argument("--headless=new")  # Comment this line to debug
    driver = webdriver.Firefox(options=options)

    login(driver)

    print("Login Successfully")

    solved_list: dict = get_solved_list(driver)
    print("Accepted answers was retrived")

    create_repository()

    for language in solved_list:
        pointer = 0
        questions_list = solved_list[language]
        while pointer < len(questions_list):
            try:
                go_to_page_with_code(
                    driver, question_id=questions_list[pointer], language=language
                )
                code, category_type, code_title = get_question_information(
                    driver, question_id=questions_list[pointer]
                )
                question_number = code_title.split()[1]

                add_question(category_type, question_number, language, code)
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
