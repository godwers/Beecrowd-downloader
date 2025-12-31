from selenium import webdriver
from selenium.webdriver.common.by import By
from time import sleep
from modules.login import login
from modules.question_list import get_solved_list
from modules.repository import create_repository
from modules.constants import LANGUAGE_ID


def main() -> None:
    options = webdriver.FirefoxOptions()
    options.add_argument("--headless=new")  # Comment this line to debug
    driver = webdriver.Firefox(options=options)

    login(driver)

    print("Login Successfully")

    solved_list = get_solved_list(driver)
    print("Accepted answers was retrived")
    print(solved_list)

    # create_repository()

    for language in solved_list:
        pointer = 0
        questions_list = solved_list[language]
        while pointer < len(questions_list):
            answer_url = f"https://judge.beecrowd.com/pt/runs?problem_id={questions_list[pointer]}&answer_id=1&language_id={LANGUAGE_ID[language]}"
            driver.get(answer_url)
            resolucao_id = driver.find_element(By.CLASS_NAME, "id").text
            pointer += 1

    driver.close()


if __name__ == "__main__":
    main()
