import json
from datetime import datetime


def is_results_file_valid():
    # The function was used for checking file's validation.
    # It was necessary to check the cases when in the result file pair of values don't equal.
    # It was assumed that we have only pair of values [number1, number1; number2, number2]

    with open("results_RUN.txt", "r", encoding="utf-8-sig") as f_results:
        f_lines = f_results.readlines()
        for idx in range(0, len(f_lines), 2):
            person_start_nmb = int(f_lines[idx].split(' ')[0])  # took number of person
            person_finish_nmb = int(f_lines[idx + 1].split(' ')[0])

            if person_start_nmb != person_finish_nmb:
                return False
    return True


def open_results_fill_the_dict():
    with open("results_RUN.txt", "r", encoding="utf-8-sig") as f_results:
        d_competitors = dict()
        f_lines = f_results.readlines()
        for idx in range(0, len(f_lines), 2):
            person_start = f_lines[idx].split(' ')
            person_finish = f_lines[idx + 1].split(' ')
            person_result_t = datetime.strptime(person_finish[2], "%H:%M:%S,%f\n") - datetime.strptime(person_start[2],
                                                                                                       "%H:%M:%S,%f\n")
            d_competitors[person_start[0]] = [person_start[0], person_result_t]

        # sort by time
        return dict(sorted(d_competitors.items(), key=lambda t: t[1][1]))


def open_json_add_to_dict(d_competitors: dict):
    with open("competitors2.json", "r", encoding="utf-8") as f_json_comp:
        data = json.load(f_json_comp)
        for person in data.items():
            if person[0] not in d_competitors:
                # person with the number 266 didn't take a part in competition
                continue
            d_competitors[person[0]].append(str(person[1]['Name']))
            d_competitors[person[0]].append(str(person[1]['Surname']))


if is_results_file_valid():
    competitors = open_results_fill_the_dict()
    open_json_add_to_dict(competitors)

    place_num = 1
    print('-----------------------------------------------------------------------------')
    print('| Занятое место | Нагрудный номер  |    Имя     |   Фамилия    |  Результат  |')
    print('-----------------------------------------------------------------------------')
    for person in competitors.items():
        print(f'|{place_num:15}|', f'{person[0]:17}|', f'{person[1][3]:11}|', f'{person[1][2]:13}|',
              f' {datetime.strptime(str(person[1][1]), "%H:%M:%S.%f").strftime("%M:%S,%f")[:-4]:11}|')
        place_num = place_num + 1
    print('-----------------------------------------------------------------------------')
