import subprocess

from errors import PARSE_ERROR, LOG
from construct import ConstructFileToProduction
from finder import HTMLClassFinder

class Parser:


    def __init__(self, content_html: str or None, content_css: str or None, cout: str or None, filename_css=None, filename_html=None, folder_html=None, folder_css=None) -> str:
        if all((filename_html, folder_html)) or all((filename_css, folder_css)) == True:
            LOG(PARSE_ERROR().ERROR_TWO_VALUES())
        if filename_html:
            self.filename_html = filename_html
            self.data = self.open_file(self.filename_html)
        elif folder_html:
            try:
                files = subprocess.check_output("cd %s; find *.html" % folder_html, stderr=subprocess.STDOUT, shell=True, encoding="utf-8").split("\n")
            except FileNotFoundError or FileExistsError or Exception as err:
                LOG(PARSE_ERROR().ERROR_WITH_ARG(err))
            self.filename_html = files
            self.data = self.open_folder(self.filename_html)
        else:
            self.content_html = content_html
            self.data = self.prettify(self.content_html)
        if filename_css:
            self.filename_css = filename_css
            self.content = self.open_file(self.filename_css)
        elif folder_css:
            try:
                files = subprocess.check_output("cd %s; find *.css" % folder_css, stderr=subprocess.STDOUT, shell=True, encoding="utf-8").split("\n")
            except FileExistsError or FileNotFoundError or Exception as err:
                LOG(PARSE_ERROR().ERROR_WITH_ARG(err))
            self.filename_css = files
            self.content = self.open_folder(self.filename_css)
        else:
            self.content_css = content_css
            self.content = self.prettify(self.content_css)
        self.cout = cout


    def open_folder(self, folder: list) -> str:
        content_list = str()
        for elem in folder:
            with open(elem, "r", encoding="utf-8") as file:
                content = file.read()
                content_prettified = self.prettify(content)
            content_list += content_prettified
        return content_list
    

    def open_file(self, filename: str) -> str:
        try:
            with open(filename, "r", encoding="utf-8") as file:
                content = file.read()
            data_prettified = self.prettify(content)
            return data_prettified
        except FileNotFoundError or FileExistsError or Exception as err:
            LOG(PARSE_ERROR().ERROR_WITH_ARG(err))


    def prettify(self, data: str or list) -> str:
        if type(data) == list:
            data_joined = "".join(data)
            return data_joined
        elif type(data) == str:
            return data
        else:
            LOG(PARSE_ERROR().ERROR_WITH_ARG(ValueError(data)))


    def from_html_find_in_css(self):
        response = HTMLClassFinder(self.data, self.content, self.cout).finder()
        return response


    def construct_css(self):
        response = ConstructFileToProduction(self.content, self.cout).construct_data()
        return response