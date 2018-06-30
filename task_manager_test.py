
from app.web_ui.gen_report_file import *


def main():
    r = GenReport()
    print(r.report_file_name)
    print(r.report_path)
    r.gen_report()


if __name__ == '__main__':
    main()
