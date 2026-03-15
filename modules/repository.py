import os
import sys
import asyncio

from .constants import LANGUAGE_EXTENSION, LANGUAGE_COMMENT

if sys.platform == "win32":
    home_path = os.environ["%USERPROFILE%"]
else:  # assuming if you use linux/macos because they are based on unix
    home_path = os.environ["HOME"]

path = os.path.join(home_path, "beecrowd_repository")
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


async def _write_file(language: str, code: str, question_title) -> None:
    with open(f"resolucao{LANGUAGE_EXTENSION[language]}", "w", encoding="utf-8") as f:
        f.write(f"{LANGUAGE_COMMENT[language]} {question_title}\n")
        f.write(code)


async def create_repository() -> None:
    try:
        os.mkdir(path)
        os.chdir(path)

        for folder_unique in folders:
            os.mkdir(folders[folder_unique])
    except FileExistsError:
        print("Repository already exist!")
        os.chdir(path)


async def add_question(
    question_type: str,
    question_number: str,
    language: str,
    code: str,
    question_title: str,
) -> None:
    question_title = _sanitize_question_title(question_title)
    _go_to_category_path(question_type)
    task_write_file = asyncio.create_task(_write_file(language, code, question_title))
    question_path = f"beecrowd_{question_number}"
    try:
        os.mkdir(question_path)
    except FileExistsError:
        pass
    finally:
        os.chdir(question_path)

    await task_write_file
    #print(os.getcwd())
    _go_to_parent_path()
