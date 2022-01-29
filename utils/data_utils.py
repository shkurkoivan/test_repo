import copy
import random


def prepare_invalid_data_for_post_character():
    list_with_ivalid__data = []
    valid_data = {"name": "TestUserInvalid", "universe": "Marvel Universe",
                  "education": "High school (unfinished)", "weight": random.choice([60, 150]),
                  "height": random.choice([1.93, 2.5]), "identity": "Publicly known"}

    #  Создаем список словарей, в каждом случайно удаляя required поле
    for i in range(0, len(valid_data)):
        list_with_ivalid__data.append((copy.deepcopy(valid_data)))
        list_with_ivalid__data[i]["name"] += str(i+1)
        list_with_ivalid__data[i][random.choice(list(valid_data.keys()))] = ""
    # Для пары полей применяем неверный тип содержимого
    list_with_ivalid__data[2][random.choice(["name", "universe,", "education"])] = random.choice([5, 2.5])
    list_with_ivalid__data[4][random.choice(["height", "weight,"])] = "invalid"
    return list_with_ivalid__data
