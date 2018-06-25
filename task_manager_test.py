import json
from app.web_ui.scan_task_manager import *


def main():
    m = ScanTaskManager()

    print(m.scan_tasks_file)
    # task_name, _ = m.get_last_task()
    # task_info = m.get_task_info(task_name)
    #
    # result = m.get_task_result(task_name)
    # print(result)
    #
    # print(ScanSetting().get_scan_setting())
    # print(ScanResult().get_scan_result())
    #
    # m.add_new_task("scan1")
    # m.save_task()


if __name__ == '__main__':
    main()
