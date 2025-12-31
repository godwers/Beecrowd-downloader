import os


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


def create_repository() -> None:
    try:
        os.mkdir(path)
        os.chdir(path)

        for folder_unique in folders:
            os.mkdir(folders[folder_unique])
    except FileExistsError:
        print("Folder already exist!")
        os.chdir(path)
