import json, os, time


def singleton(cls):
    _instance = {}

    def _singleton(*args, **kargs):
        if cls not in _instance:
            _instance[cls] = cls(*args, **kargs)
        return _instance[cls]

    return _singleton


class TaskInfo(object):
    def __init__(self, task_info_dict=None):
        if task_info_dict:
            self.task_info_dict = task_info_dict
            self.start_url = self.task_info_dict["ScanSetting"]["StartURL"]
            self.scan_policy = self.task_info_dict["ScanSetting"]["ScanPolicy"]
            self.scan_result_file = self.task_info_dict["ScanResultFile"]
            self.timestamp = self.task_info_dict["Timestamp"]
        else:
            self.task_info_dict = {}
            self.start_url = ""
            self.scan_policy = ""
            self.scan_result_file = "scan_result.json"
            self.timestamp = time.time()
            self.task_info_dict["ScanSetting"] = {}
            self.task_info_dict["ScanSetting"]["StartURL"] = self.start_url
            self.task_info_dict["ScanSetting"]["ScanPolicy"] = self.scan_policy
            self.task_info_dict["ScanResultFile"] = self.scan_result_file
            self.task_info_dict["Timestamp"] = self.timestamp

    def get_task_info_dict(self):
        self.task_info_dict["ScanSetting"]["StartURL"] = self.start_url
        self.task_info_dict["ScanSetting"]["ScanPolicy"] = self.scan_policy
        self.task_info_dict["ScanResultFile"] = self.scan_result_file
        self.task_info_dict["Timestamp"] = self.timestamp
        return self.task_info_dict


@singleton
class ScanSetting:
    def __init__(self, url="", policy="Normal"):
        self.start_url = url
        self.scan_policy = policy

    def get_scan_setting(self):
        return (self.start_url, self.scan_policy)


@singleton
class ScanResult:
    def __init__(self):
        self.wvs_result_list = []

    def has(self, result):
        identifier = "{}_{}".format(result["VulType"], result["VulUrl"])
        for res in self.wvs_result_list:
            res_identifier = "{}_{}".format(res["VulType"], res["VulUrl"])
            print(res_identifier, identifier)
            if res_identifier == identifier:
                return True

        return False

    def add_scan_result(self, result):
        existed = self.has(result)
        if not existed:
            self.wvs_result_list.append(result)
        else:
            pass

    def get_scan_result(self):
        return self.wvs_result_list


class ScanTaskManager(object):
    def __init__(self, filepath=None):
        if filepath:
            self.scan_tasks_file = filepath
        else:
            self.scan_tasks_file = self.__get_tasks_file_path()
        self.scan_task_list = self.__get_task_list()
        self.__last_task = self.get_last_task()

    def __get_tasks_file_path(self):
        return os.path.join(os.getcwd(), "scan_task", "task_list.json")

    def __get_task_list(self):
        with open(self.scan_tasks_file, 'r') as rf:
            task_dict = json.load(rf)
            return sorted(task_dict.items(), key=lambda d: d[1])

    def __gen_task_info_path(self, task_name):
        return os.path.join(os.getcwd(), "scan_task", task_name)

    def get_task_info(self, task_name):
        with open(os.path.join(self.__gen_task_info_path(task_name), "task_info.json"), 'r') as rf:
            task_info_json = json.load(rf)
            task_info = TaskInfo(task_info_json)
            ScanSetting(task_info.start_url, task_info.scan_policy)
            return task_info

    def get_task_result(self, task_name):
        task_info = self.get_task_info(task_name)
        with open(os.path.join(self.__gen_task_info_path(task_name), task_info.scan_result_file), 'r') as rf:
            ScanResult().wvs_result_list = json.load(rf)
            return ScanResult().wvs_result_list

    def add_new_task(self, task_name):
        os.mkdir(self.__gen_task_info_path(task_name))
        self.scan_task_list.append((task_name, time.time()))

    def save_task(self):
        task_name = self.get_last_task()[0]
        self.save_task_list()

        with open(os.path.join(self.__gen_task_info_path(task_name), "task_info.json"), 'w') as wf:
            task_info = TaskInfo()
            task_info.start_url, task_info.scan_policy = ScanSetting().get_scan_setting()

            task_info_json = task_info.get_task_info_dict()
            json.dump(task_info_json, wf)

        with open(os.path.join(self.__gen_task_info_path(task_name), task_info.scan_result_file), 'w') as wf:
            json.dump(ScanResult().get_scan_result(), wf)

    def save_task_list(self):
        task_dict = {}
        for task in self.scan_task_list:
            task_dict[task[0]] = task[1]

        with open(self.scan_tasks_file, 'w') as wf:
            json.dump(task_dict, wf)

    def get_last_task(self):
        return self.scan_task_list[::-1][0]


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

