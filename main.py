from time import sleep
from sys import argv
import asyncio

from selenium import webdriver
from selenium.common.exceptions import TimeoutException

from modules.login import login
from modules.question_list import get_solved_list
from modules.repository import create_repository, add_question
from modules.download import get_question_information, go_to_page_with_code
from modules.addons import add_ublock,remove_ublock


async def main(driver) -> None:
    task_create_repository = asyncio.create_task(create_repository())
    login(driver)

    print("Login Successfully")

    solved_list: dict = get_solved_list(driver)
    print("Accepted answers was retrived")

    await task_create_repository


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

                await add_question(category_type, question_number, language, code, code_title)
                print(code_title)
                print(category_type)
                print(code)

                pointer += 1
                sleep(1)
            except TimeoutException:
                continue

"""
TODO: Add UBlock Origin bc firefox is using 4gb of ram
"""
if __name__ == "__main__":
    options = webdriver.FirefoxOptions()
    options.timeouts = { "implicit" : 5432 } # in miliseconds
    options.rage_load_strategy = 'eager'

    if not "--debug" in argv:
        options.add_argument("--headless=new")          

    with webdriver.Firefox(options=options) as driver:
        addon_file_path = add_ublock(driver)
        asyncio.run(main(driver))
        remove_ublock(addon_file_path)


