from time import sleep
from sys import argv
from asyncio import create_task,run

from selenium import webdriver
from selenium.common.exceptions import TimeoutException

from modules.login import login
from modules.answers_list import get_solved_list
from modules.repository import create_repository, add_question, start_git_repository
from modules.scrape_code import get_question_information, go_to_page_with_code
from modules.addons import add_ublock,remove_ublock


async def main(driver) -> None:
    task_create_repository = create_task(create_repository())
    login(driver)

    print("Login Successfully")

    solved_list: dict[str,list[int]] = get_solved_list(driver)
    print("Accepted answers was retrived")

    await task_create_repository
    git_repository = start_git_repository()


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

                await add_question(category_type, question_number,
                                   language, code, code_title,
                                   git_repository)

                print(code_title)
                print(category_type)
                print(code)

                pointer += 1
                sleep(1)
            except TimeoutException:
                continue

if __name__ == "__main__":
    options = webdriver.FirefoxOptions()
    options.timeouts = { "implicit" : 5432 } # in miliseconds

    if not "--debug" in argv:
        options.add_argument("--headless=new")          
        options.rage_load_strategy = 'none'

    with webdriver.Firefox(options=options) as driver:
        addon_file_path = add_ublock(driver)
        run(main(driver))
        remove_ublock(addon_file_path)



