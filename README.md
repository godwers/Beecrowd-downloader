# Beecrowd Downloader
This is a repository inspired by [Luan Simões's repository](https://github.com/Snizi/Beecrowd-Code-Downloader),
based on this [repository for IFMG students](https://github.com/gabbymagica/IFNeves-beecrowd).

##  Dependencies
`uv` for managing the packages. [See here how to download](https://docs.astral.sh/uv/getting-started/installation/)<br>
`>=Python 3.14` for Selenium and Getpass<br>
`Firefox` for the webdriver<br>
`>=git 1.7.0` for managing the repository<br>

## How to use:
1. Clone the latest release 
```
git clone https://github.com/godwers/Beecrowd-downloader.git
```
2. Create a virtual enviroment in Python 
```
uv venv
```
3. Activate the virtual enviroment
> Now it depends of the OS that you are using to activate it.<br> 
Please look into the [Python virtual enviroment docs](https://docs.python.org/3/library/venv.html#how-venvs-work)
```bash
Example on Linux:
$ source .venv/bin/activate
```
4. Download the requirements for the project using `uv`
```
uv pip install -r pyproject.toml
```
5. Now you can run the code!!!!11111
```
python main.py
```
