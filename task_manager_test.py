import json
from app.web_ui.scan_task_manager import *


def main():
    m = ScanTaskManager()

    print(m.scan_tasks_file)
    task_list = m.scan_task_list
    print("Task List::\t{}".format(task_list))

    task_name, _ = m.get_last_task()
    print("Last Task Name::\t{}".format(task_name))
    task_info,_,_ = m.get_task_info(task_name)
    print("Last Task Info::\t{}".format(task_info.get_task_info_dict()))

    m.add_new_task("scan_test")
    ScanSetting().set_scan_setting(url="http://127.0.0.1:80", policy="Full")
    m.save_task()
    task, _ = m.get_last_task()
    ScanSetting().start_url="http://127.0.0.1:80"
    # ScanSetting().set_scan_setting(task_info.start_url,"Full")


    m.save_task()



    info,setting, result = m.get_task_info("Scan_0")
    print("Last Task Info::\t{}".format(info.get_task_info_dict()))
    print("Last Setting Info::\t{}".format(ScanSetting().get_scan_setting()))

    info,setting, result = m.get_task_info()
    print("Last Task Info::\t{}".format(info.get_task_info_dict()))

    m.del_task("scan_test")

    #
    # print(ScanSetting().get_scan_setting())
    # print(ScanResult().get_scan_result())
    #
    # m.add_new_task("scan1")
    # m.save_task()


if __name__ == '__main__':
    main()
