import os
import sys
import asyncio

from git import Repo

from .constants import LANGUAGE_EXTENSION, LANGUAGE_COMMENT

repository_name = "beecrowd_repository"
if sys.platform == "win32":
    home_path = os.environ["%USERPROFILE%"]
else:  # assuming if you use linux/macos because they are based on unix
    home_path = os.environ["HOME"]

path = os.path.join(home_path, repository_name)
folders = {
    "INICIANTE": "1. Iniciante",
    "AD-HOC": "2. AD-HOC",
    "STRINGS": "3. Strings",
    "ESTRUTURAS E BIBLIOTECAS": "4. Estruturas e Bibliotecas",
    "MATEMÁTICA": "5. Matemática",
    "PARADIGMAS": "6. Paradigmas",
    "GRAFOS": "7. Grafos",
    "GEOMETRIA COMPUTACIONAL": "8. Geometria Computacional",
    "SQL": "9. SQL",
}


def _go_to_parent_path() -> None:
    os.chdir(path)


def _sanitize_question_title(question_title: str) -> str:
    novo_texto = ""

    for index, char in enumerate(question_title):
        if char == " " and question_title[index + 1] == " ":
            continue
        elif char == "Í" and question_title[index : index + 4] == "ÍVEL":
            novo_texto += question_title[index:].lower()
            break
        novo_texto += char

    return novo_texto


def _go_to_category_path(folder: str) -> None:
    os.chdir(os.path.join(path, folders[folder]))


async def _write_file(language: str, 
                      code: str, 
                      question_title: str,
                      question_number: str,
                      git_repository : Repo) -> None:
    task_update_git_repository = asyncio.create_task(_update_git_repository(git_repository,
                                                                            question_number,
                                                                            language,
                                                                            os.getcwd().split(repository_name)[1][1:]))
    with open(f"resolucao{LANGUAGE_EXTENSION[language]}", "w", encoding="utf-8") as f:
        f.write(f"{LANGUAGE_COMMENT[language]} {question_title}\n")
        f.write(code)
    await task_update_git_repository

async def _update_git_repository(git_repository : Repo,
                                 question_number : str,
                                 code_language: str,
                                 file_path: str) -> None:
    git_repository.index.add(file_path)
    git_repository.index.commit(f"Added {question_number} {code_language} version")
    


async def create_repository() -> None:
    try:
        os.mkdir(path)
        Repo.init(path)
    except FileExistsError:
        print("Repository already exist!")
        os.chdir(path)
        return 

    os.chdir(path)
    for folder_unique in folders:
        os.mkdir(folders[folder_unique])


def start_git_repository() -> Repo:
    return Repo(path)

async def add_question(
    question_type: str,
    question_number: str,
    language: str,
    code: str,
    question_title: str,
    git_repository: Repo,
) -> None:
    question_title = _sanitize_question_title(question_title)
    _go_to_category_path(question_type)
    task_write_file = asyncio.create_task(_write_file(language, code, question_title,question_number,git_repository))
    question_path = f"beecrowd_{question_number}"
    try:
        os.mkdir(question_path)
    except FileExistsError:
        pass
    finally:
        os.chdir(question_path)

    await task_write_file
    _go_to_parent_path()
