import requests
from IPython.display import HTML

def update(module=""):
    """Fetch modules from Github and write them to folder"""
    nba = requests.get("https://raw.githubusercontent.com/Yoonsen/Modules/master/{module}.py".format(module=module))
    
    if nba.status_code == 200:
        nba = nba.text
        with open('{m}.py'.format(m=module),'w', encoding='UTF-8') as pyfile:
            pyfile.write(nba)
        print("Updated file {module}.py".format(module=module))
    else:
        print("An error occured ", module, nba.status_code)
    return

def css():
    """Associate a css stylesheet with the notebook"""
    css_file = requests.get("https://raw.githubusercontent.com/Yoonsen/Modules/master/css_style_sheets/monokai.css")
    res = ""
    if css_file.status_code == 200:
        res = css_file.text
    return HTML(res)

update("nbtext")
update("nbpictures")