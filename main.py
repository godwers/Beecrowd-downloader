import json
import os
from time import sleep
from sys import argv
from asyncio import create_task,run

from selenium import webdriver

from modules.login import login
from modules.answers_list import get_solved_list
from modules.repository import create_repository, add_question, start_git_repository
from modules.scrape_code import get_question_information, go_to_page_with_code
from modules.addons import add_ublock,remove_ublock


async def main(driver) -> None:
    task_create_repository = create_task(create_repository())
    login(driver)

    print("Login Successfully")

    solved_list: dict[str,list[dict[int,str]]] = get_solved_list(driver)
    print("Accepted answers was retrived")

    await task_create_repository
    git_repository = start_git_repository()

    if not os.path.exists("current_answers.json"):
        old_answers = solved_list 
    else:
        with open("current_answers.json","r",encoding="utf-8") as file:
            old_answers = json.load(file)

    for language in solved_list:
        pointer = 0
        questions_list : list[dict[int,str]] = solved_list[language]
        while pointer < len(questions_list):
            _ = questions_list[pointer]
            question_id = list(_.keys())[0]
            unique_identifier = _.get(question_id)

            old_unique_identifier = old_answers[language]
            old_unique_identifier = old_unique_identifier[pointer]

            if old_unique_identifier[question_id] == unique_identifier and (
                    os.path.exists("current_answers.json")
            ):
                pointer += 1
                continue

            go_to_page_with_code(driver,unique_identifier) # pyright: ignore[]
            code, category_type, code_title = get_question_information(
                driver, question_id=question_id
            )
            question_number = code_title.split()[1]

            await add_question(category_type, question_number, # pyright: ignore[]
                               language, code, code_title,
                               git_repository)

            print(code_title)
            print(category_type)
            print(code)

            pointer += 1
            sleep(1)
    with open("current_answers.json","w",encoding="utf-8") as f:
        json.dump(solved_list,f,indent=4)

if __name__ == "__main__":
    options = webdriver.FirefoxOptions()
    options.timeouts = { "implicit" : 5432 } # in miliseconds

    if "--debug" not in argv:
        options.add_argument("--headless=new")          
        options.rage_load_strategy = 'none'

    with webdriver.Firefox(options=options) as driver:
        addon_file_path = add_ublock(driver)
        driver.implicitly_wait(5)
        run(main(driver))
        remove_ublock(addon_file_path)



