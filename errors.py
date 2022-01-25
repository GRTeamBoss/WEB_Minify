from time import ctime

class PARSE_ERROR:
    OK = '\033[92m'
    FAIL = '\033[91m'
    WARNING = '\033[93m'
    RESET = '\033[0m'


    def ERROR_WITH_ARG(self, cause):
        error = self.FAIL + str(cause) + self.RESET
        return error


    def ERROR_TWO_VALUES(self):
        err = self.FAIL + "incorrect:" + self.RESET + "filename_html and folder_html or filename_css or folder_css all 'True'\n" +\
            self.OK + "correct:" + self.RESET + "filename_html or folder_html 'True' and filename_css or folder_css 'True'"
        return err


    def ERROR_NOT_CLASS_IN_HTML(self):
        err = self.FAIL + "html" + self.RESET + "file not has" + self.WARNING + "'class'" + self.RESET
        return err


class LOG:

    __debug = "class_parse_log.txt"
    __debug_cmd = "class_parse_log_cmd.txt"
    OK = '\033[92m'
    WARNING = '\033[93m'
    RESET = '\033[0m'


    def __init__(self, cause: str, title="FAIL") -> None:
        if title=="FAIL":
            title_cmd = self.WARNING + title + self.RESET
        elif title=="WARNING":
            title_cmd = self.WARNING + title + self.RESET
        elif title=="SUCCESS":
            title_cmd = self.OK + title + self.RESET
        log = "[*] [{}]\n[{}] ---{}---\n".format(ctime(), title, cause)
        log_cmd = "[*] [{}]\n[{}] ---{}---\n".format(ctime(), title_cmd, cause)
        print(log, file=open(self.__debug, "a+", encoding="utf-8"))
        print(log_cmd, file=open(self.__debug_cmd, "a+", encoding="utf-8"))