import os
from .constants import LANGUAGE_EXTENSION

current_directory = os.getcwd()
path = os.path.join(current_directory, "beecrowd_repository")
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


def go_to_parent_path() -> None:
    os.chdir(path)


def go_to_category_path(folder: str) -> None:
    os.chdir(os.path.join(path, folders[folder]))


def write_file(language: str, code: str) -> None:
    with open(f"resolucao{LANGUAGE_EXTENSION[language]}", "w", encoding="utf-8") as f:
        f.write(code)


def create_repository() -> None:
    try:
        os.mkdir(path)
        os.chdir(path)

        for folder_unique in folders:
            os.mkdir(folders[folder_unique])
    except FileExistsError:
        print("Folder already exist!")
        os.chdir(path)


def add_question(
    question_type: str, question_number: str, language: str, code: str
) -> None:
    go_to_category_path(question_type)
    question_path = f"beecrowd_{question_number}"
    try:
        os.mkdir(question_path)
    except FileExistsError:
        pass
    finally:
        os.chdir(question_path)

    write_file(language, code)
    go_to_parent_path()
