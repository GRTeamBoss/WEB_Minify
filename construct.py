from re import findall
import subprocess

from errors import LOG, PARSE_ERROR


class ConstructFileToProduction:


    def __init__(self, data: str or list or None, cout: str or None, filename=None, folder=None) -> None:
        self.data = data
        self.cout = cout
        if filename:
            with open(filename, "r", encoding="utf-8") as file:
                self.data = file.read()
        elif folder:
            try:
                file_list = subprocess.check_output("cd {}; ls", stderr=subprocess.STDOUT, shell=True).split("\n")
            except FileNotFoundError or FileExistsError or Exception as err:
                LOG(PARSE_ERROR().ERROR_WITH_ARG(err))
            self.data = str()
            for elem in file_list:
                with open(elem, "r", encoding="utf-8") as file:
                    self.data += file.read()



    def construct_css(self):
        if type(self.data) == list:
            data_css = str()
            for elem in self.data:
                data_css += "".join(findall(r"[\.\>\&\*\+\,\@\(\)\:\-\{\}\;\/\#\w]+", elem))
            LOG("construcs_data -> list", title="SUCCESS")
            if self.cout:
                print(data_css, file=open(self.cout, "w", encoding="utf-8"))
            return data_css
        elif type(self.data) == str:
            data_css = "".join(findall(r"[\.\>\&\*\+\,\@\(\)\:\-\{\}\;\/\#\w]+", self.data))
            LOG("construcs_css -> str", title="SUCCESS")
            if self.cout:
                print(data_css, file=open(self.cout, "w", encoding="utf-8"))
            return data_css
        else:
            LOG(PARSE_ERROR().ERROR_WITH_ARG(ValueError(self.data)))


    def construct_js(self) -> str:
        regex = r"[^ \t\r\n\f]*"
        print("[*] Debug: data_js ->", findall(regex, self.data))
        data_js = str()
        finded_refresh = list()
        if type(self.data)==list:
            for elem in self.data:
                finded = findall(regex, elem)
                for _ in range(len(finded)):
                    for num in range(len(finded)):
                        if len(finded[num]) == 0:
                            finded.pop(num)
                            break
                for num in range(len(finded)):
                    if finded[num]:
                        if finded[num][-1] in ";(){}+=*/\'\"":
                            pass
                        elif num < len(finded)-1:
                            if finded[num+1]:
                                if finded[num+1] in "=+=-=*=/(){}++--/**":
                                    pass
                                else:
                                    finded[num+1] = " " + finded[num+1]
                for el in finded:
                    finded_refresh.append(el)
                data_js += "".join(finded_refresh)
            LOG("construct_js -> list", title="SUCCESS")
            if self.cout:
                print(data_js, file=open(self.cout, "w", encoding="utf-8"))
            return data_js
        elif type(self.data)==str:
            finded = findall(regex, self.data)
            for _ in range(len(finded)):
                    for num in range(len(finded)):
                        if len(finded[num]) == 0:
                            finded.pop(num)
                            break
            for num in range(len(finded)):
                if finded[num]:
                    if finded[num][-1] in ";{}()+=*/\'\"":
                        pass
                    elif num < len(finded)-1:
                        if finded[num+1]:
                            if finded[num+1] in "=+=-=*=/(){}++--/**":
                                pass
                            else:
                                finded[num+1] = " " + finded[num+1]
            for el in finded:
                finded_refresh.append(el)
            data_js = "".join(finded_refresh)
            LOG("contsruct_js -> str", title="SUCCESS")
            if self.cout:
                print(data_js, file=open(self.cout, "w", encoding="utf-8"))
            return data_js
        else:
            LOG(PARSE_ERROR().ERROR_WITH_ARG(ValueError(self.data)))