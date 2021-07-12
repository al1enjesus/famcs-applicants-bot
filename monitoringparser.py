import requests
from bs4 import BeautifulSoup


class Parser:
    url = "https://abit.bsu.by/formk1?id=1"
    template = ["Специальность",
                "План приема на бюджет",
                "Целевики",
                "План приема на платное",
                "Всего подано заявлений",
                "Целевики",
                "Олимпиадники",
                "Вне конкурса",
                "391+",
                "390-381",
                "380-371",
                "370-361",
                "360-351",
                "350-341",
                "340-331",
                "330-321",
                "320-311",
                "310-301",
                "300-291",
                "290-281",
                "280-271",
                "270-261",
                "260-251",
                "250-241",
                "240-231",
                "230-221",
                "220-211",
                "210-201",
                "200-191",
                "190-181",
                "180-171",
                "170-161",
                "160-151",
                "150-141",
                "140-131",
                "130-121",
                "120"
                ]

    def __call__(self, spec_name, grade):
        raw = requests.get(Parser.url)
        src = raw.text.encode('cp1251')
        soup = BeautifulSoup(src, features='lxml')
        tr_list = soup.find_all('tr')
        self.last_update_time = soup.find('span', {'id': 'Abit_K11_lbCurrentDateTime'}).text

        print("Parsed")

        for tr in tr_list:
            for td in tr.find_all('td'):
                if td.string == spec_name:
                    return self.pretty_formatting(tr, grade)

    def pretty_formatting(self, tr, grade):
        pos = Parser.template.index(grade)
        tds = tr.find_all('td')

        answer = "Последнее обновление: {}\n".format(self.last_update_time)

        better_res = 0
        for i in range(len(tds)):
            if tds[i].string is not None:
                if (i > 5) and (i < pos) and (i != 7):
                    better_res += int(tds[i].string)
                answer += "{}: {}\n".format(Parser.template[i], tds[i].string)

        if tds[pos].string is None:
            your_grade_lvl = 0
        else:
            your_grade_lvl = tds[pos].string

        answer += "Вы указали балл: {}\nВас опережает {} + {} человек".format(grade, better_res, your_grade_lvl)

        return answer
