import requests
from bs4 import BeautifulSoup
from time import perf_counter as clock


class Parser:
    def __init__(self) -> None:
        self.url = "https://abit.bsu.by/formk1?id=1"
        self.template = [
            "План приема на факультет",
            "Подано заявлений",
            "Специальность",
            "План приема на бюджет",
            "Целевики",
            "План приема на платное",
            "Всего подано заявлений",
            "Целевики",
            "Олимпиадники",
            "Вне конкурса",
            "391+",
            "390-386",
            "385-381",
            "380-376",
            "375-371",
            "370-366",
            "365-361",
            "360-356",
            "355-351",
            "350-346",
            "345-341",
            "340-336",
            "335-331",
            "330-326",
            "325-321",
            "320-316",
            "315-311",
            "310-306",
            "305-301",
            "300-296",
            "295-291",
            "290-286",
            "285-281",
            "280-276",
            "275-271",
            "270-266",
            "265-261",
            "260-256",
            "255-251",
            "250-246",
            "245-241",
            "240-236",
            "235-231",
            "230-226",
            "225-221",
            "220-216",
            "215-211",
            "210-206",
            "205-201",
            "200-196",
            "195-191",
            "190-186",
            "185-181",
            "180-176",
            "175-171",
            "170-166",
            "165-161",
            "160-156",
            "155-151",
            "150-146",
            "145-141",
            "140-136",
            "135-131",
            "130-126",
            "125-121",
            "120-",
        ]
        self.last_update_time, self.last_fetch = self.fetch_data()

    def __call__(self, spec_name, grade):
        if self.last_update_time - clock() < 60:
            self.last_update_time, self.last_fetch = self.fetch_data()

        for row in self.last_fetch:
            for cell in row.find_all("td"):
                if cell.string == spec_name:
                    return self.pretty_formatting(row, grade)

    def fetch_data(self):
        raw = requests.get(self.url)
        src = raw.text.encode("cp1251")
        soup = BeautifulSoup(src, features="lxml")
        rows = soup.find_all("tr")
        return clock(), rows

    def pretty_formatting(self, row, grade):
        user_grade_index = self.template.index(grade)
        cells = row.find_all("td")
        answer = ""
        better_res = 0

        for index, cell in enumerate(cells):
            if cell.string is not None:
                if (index > 6) and (index < user_grade_index):
                    better_res += int(cells[index].string)
                answer += "{}: {}\n".format(self.template[index], cell.string)

        if cells[user_grade_index].string is None:
            user_grade_lvl = 0
        else:
            user_grade_lvl = cells[user_grade_index].string

        answer += "Вы указали балл: {}\nВас опережает {} + {} человек".format(
            grade, better_res, user_grade_lvl
        )

        return answer
