import math
import requests
import numpy as np


class GetCompatibility:
    def __init__(self, data):
        self.data = data

    def get_scores(self):
        results = []
        # Проходим по каждому пользователю
        for user in self.data:
            zodiac_sign = user[0]
            # Создаем список баллов для текущего знака зодиака
            scores = []
            # Проходим по всем пользователям и собираем баллы для текущего знака зодиака
            for other_user in self.data:
                if other_user[0] != zodiac_sign:  # Исключаем самого себя
                    score = other_user[1].get(zodiac_sign)
                    if score is not None:
                        scores.append(score)
            results.append(scores)
        return results

    def calculate_similarity(self, numbers):
        """Вычисляет процентную схожесть для одного списка."""
        if len(numbers) == 0:
            return 0
        mean = np.mean(numbers)
        std_dev = np.std(numbers)
        coefficient_of_variation = (std_dev / mean) * 100  # CV в процентах
        similarity_percentage = max(0, 100 - coefficient_of_variation)
        return similarity_percentage

    def get_similarity(self):
        """Вычисляет общую схожесть для столбцов."""
        list_of_lists = self.get_scores()
        # Транспонируем список списков, чтобы работать со столбцами
        columns = np.array(list_of_lists).T
        similarities = [self.calculate_similarity(
            column) for column in columns]
        overall_similarity = np.mean(similarities)
        return overall_similarity


class GetCosmogram:
    '''Модуль рассчета космограммы человека'''
    signs = (
        "овен", "телец", "близнецы", "рак", "лев", "дева",
        "весы", "скорпион", "стрелец", "козерог", "водолей", "рыбы"
    )
    zodiac_compatibility = {
        "овен": {
            "овен": 97, "телец": 12, "близнецы": 89, "рак": 5, "лев": 92,
            "дева": 54, "весы": 7, "скорпион": 38, "стрелец": 81,
            "козерог": 4, "водолей": 76, "рыбы": 25
        },
        "телец": {
            "овен": 16, "телец": 100, "близнецы": 29, "рак": 88, "лев": 8,
            "дева": 77, "весы": 15, "скорпион": 22, "стрелец": 9,
            "козерог": 94, "водолей": 11, "рыбы": 65
        },
        "близнецы": {
            "овен": 83, "телец": 23, "близнецы": 95, "рак": 19, "лев": 91,
            "дева": 10, "весы": 87, "скорпион": 14, "стрелец": 34,
            "козерог": 21, "водолей": 90, "рыбы": 6
        },
        "рак": {
            "овен": 6, "телец": 73, "близнецы": 15, "рак": 99, "лев": 19,
            "дева": 85, "весы": 9, "скорпион": 78, "стрелец": 3,
            "козерог": 11, "водолей": 5, "рыбы": 81
        },
        "лев": {
            "овен": 96, "телец": 8, "близнецы": 33, "рак": 17, "лев": 91,
            "дева": 42, "весы": 80, "скорпион": 12, "стрелец": 98,
            "козерог": 6, "водолей": 25, "рыбы": 74
        },
        "дева": {
            "овен": 55, "телец": 78, "близнецы": 13, "рак": 93, "лев": 45,
            "дева": 88, "весы": 23, "скорпион": 84, "стрелец": 21,
            "козерог": 91, "водолей": 31, "рыбы": 19
        },
        "весы": {
            "овен": 11, "телец": 18, "близнецы": 90, "рак": 7, "лев": 89,
            "дева": 36, "весы": 82, "скорпион": 27, "стрелец": 94,
            "козерог": 9, "водолей": 87, "рыбы": 4
        },
        "скорпион": {
            "овен": 30, "телец": 10, "близнецы": 12, "рак": 88, "лев": 7,
            "дева": 95, "весы": 14, "скорпион": 97, "стрелец": 5,
            "козерог": 83, "водолей": 19, "рыбы": 99
        },
        "стрелец": {
            "овен": 78, "телец": 5, "близнецы": 18, "рак": 13, "лев": 89,
            "дева": 20, "весы": 95, "скорпион": 6, "стрелец": 92,
            "козерог": 26, "водолей": 79, "рыбы": 11
        },
        "козерог": {
            "овен": 4, "телец": 92, "близнецы": 8, "рак": 16, "лев": 11,
            "дева": 97, "весы": 18, "скорпион": 75, "стрелец": 20,
            "козерог": 85, "водолей": 28, "рыбы": 37
        },
        "водолей": {
            "овен": 79, "телец": 15, "близнецы": 82, "рак": 11, "лев": 8,
            "дева": 92, "весы": 88, "скорпион": 12, "стрелец": 77,
            "козерог": 29, "водолей": 95, "рыбы": 78
        },
        "рыбы": {
            "овен": 26, "телец": 89, "близнецы": 7, "рак": 83, "лев": 9,
            "дева": 16, "весы": 13, "скорпион": 91, "стрелец": 11,
            "козерог": 79, "водолей": 35, "рыбы": 97
        }
    }

    def __init__(self, date, addres, time):
        self.year, self.month, self.day = map(
            int, str(date).split('-'))
        self.addres = addres.split(', ')
        self.hour, self.minute = map(
            int, str(time).split(':')[:2])

    def zodiac_sign(self, degrees):
        """Определение знака зодиака на основе градуса."""
        index = int(degrees // 30)
        return self.signs[index]

    def equal_house_system(self, ascendant_deg):
        """
        Рассчитывает куспиды домов в градусах для системы равных домов.
        Каждый дом на 30 градусов вперед от Асцендента.
        """
        houses = [self.zodiac_sign((ascendant_deg + i * 30) % 360)
                  for i in [0, 1, 5, 6, 8, 9, 10]]
        return houses

    @staticmethod
    def get_geocode(name: str):
        url = f"https://nominatim.openstreetmap.org/search?q={name}&format=json&limit=1"
        headers = {'User-Agent': 'Namix project'}
        try:
            response = requests.get(url, headers=headers)
            response.raise_for_status()
            data = response.json()
            if data:
                result = data[0]
                latitude = result["lat"]
                longitude = result["lon"]
                return float(latitude), float(longitude)
            else:
                raise ValueError
        except requests.exceptions.RequestException as e:
            raise e

    def get_cosmogram(self):
        latitude, longitude = self.get_geocode(self.addres)
        JD2000 = 2451545.0
        if self.month <= 2:
            self.year -= 1
            self.month += 12
        A = math.floor(self.year / 100)
        B = 2 - A + math.floor(A / 4)
        JD = (
            math.floor(365.25 * (self.year + 4716)) +
            math.floor(30.6001 * (self.month + 1)) +
            self.day + B - 1524.5
        )
        JD += (self.hour + self.minute / 60) / 24
        T = (JD - JD2000) / 36525.0
        GST = (280.46061837 +
               360.98564736629 * (JD - JD2000) +
               0.000387933 * T**2 -
               T**3 / 38710000) % 360
        LST = (GST + longitude) % 360
        ascendant_degree = (LST + (latitude / 90) * 30) % 360
        n = 0.985647  # Средняя скорость движения Солнца (градусов в день)
        L0 = 280.46  # Средняя долгота Солнца на J2000
        M0 = 357.528  # Средняя аномалия Солнца на J2000

        D = JD - JD2000
        M = M0 + n * D  # Средняя аномалия

        C = (1.914602 - 0.004817 * (D / 36525) -
             0.000014 * (D / 36525)**2) * math.sin(math.radians(M))
        C += (
            0.019993 - 0.000101 * (D / 36525)) * math.sin(math.radians(2 * M))
        C += 0.000289 * math.sin(math.radians(3 * M))

        sun_longitude = (L0 + M + C) % 360
        return (
            self.zodiac_sign(sun_longitude),
            self.equal_house_system(ascendant_degree))

    def get_score(self):
        info = self.get_cosmogram()
        score = np.zeros((len(self.signs)))
        for sign in info[1]:
            base_values = np.array(
                list(self.zodiac_compatibility[sign].values()))
            score += base_values
        return [info[0], dict(zip(self.signs, list(map(float, score))))]
