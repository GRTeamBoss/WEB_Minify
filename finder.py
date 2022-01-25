from re import findall

from errors import PARSE_ERROR, LOG


class HTMLClassFinder:


    def __init__(self, data: str or list, content: str or list, cout: str or None) -> str:
        if data and content:
            self.data = data
            self.content = content
            self.cout = cout
        else:
            LOG(PARSE_ERROR().ERROR_WITH_ARG(ValueError))


    def __doc__(self):
        info = """
[*] data:
- html string

[*] content:
- css string

[*] cout:
- value: 'filename.css' or 'filename.txt'
only write, do not append, but you may edit this module.
Writed at production style
        """
        return info 


    def finder(self):
        data = self.data
        content = self.content


        def finder_in_html(data: str):
            data_class = list()
            data_class_refreshed = list()
            if "class=" in data:
                data_splited = findall(r"class=[\'\"][\w\-\s]+[\'\"]", data)
                for elem in data_splited:
                    data_class.append("".join(findall(r"[^ \'\"][\w\-\s]+[^ \'\"]", elem.split("class=")[1])))
                for elem in data_class:
                    for el in elem.split():
                        data_class_refreshed.append(el)
                LOG('finder_in_html', title="SUCCESS")
                return data_class_refreshed
            else:
                LOG(PARSE_ERROR().ERROR_NOT_CLASS_IN_HTML(), title="WARNING")


        def finder_in_css(data_html: list, data_css: str):
            data_result = str()
            for elem in data_html:
                regex = r"[\.\w\>\s\&\*\+\,\@\(\)\:\-]*\.%s[\.\w\s\>\*\&\+\,\:\(\)\-\@]*\{[\.\w\s\:\;\,\(\)\+\-\*\/]+\}" % elem
                finded = "".join(findall(regex, data_css))
                if finded in data_result:
                    pass
                else:
                    data_result += finded
            LOG('finder_in_css', title="SUCCESS")
            if self.cout:
                print(data_result, file=open(self.cout, 'w', encoding="utf-8"))
            return data_result


        if all((data, content)):
            data_html = finder_in_html(data)
            data_css = finder_in_css(data_html, content)
            return data_css
        else:
            return 0