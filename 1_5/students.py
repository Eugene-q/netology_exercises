import random

students = list()


def students_generator():
    titles = ['name', 'fname', 'sex', 'experience', 'grades', 'exam']
    persons = [
        ['Нюша', 'Хрюшина', 'female'],
        ['Бараш', 'Круторогов', 'male'],
        ['Крош', 'Морковкин', 'male'],
        ['Ёжик', 'Ежидзе', 'male'],
        ['Пин', 'Фатерлянд', 'male'],
        ['Лосяш', 'Копытов', 'male'],
        ['Совунья', 'Таблэткина', 'female'],
        ['Кар', 'Карыч', 'male'],
        ['Люсьен', 'Копатычев', 'male'],
    ]
    for person in persons:
        person.append(random.choice([False, True]))
        person.append(list())
        for i in range(5):
            person[4].append(random.randint(3, 10))
        person.append(random.randint(5, 10))
        students.append(dict(zip(titles, person)))


def const(in_word):
    vocabulary = {
        'GET_COMMAND': 'введите команду (h - список команд):',
        'NO_COMMAND': 'нет такой команды!',
        'AVG_EXAM': 'Спедняя оценка за экзамен',
        'AVG_GRADES': 'Средняя оценка за д/з',
        'BEST_STUDENTS': 'Лучшие студенты :',
        'male': 'у мужчин',
        'female': 'у женщин',
        False: 'у студентов без опыта',
        True: 'у студентов с опытом',
        None: '',
    }
    return vocabulary[in_word]


def avg(values):
    s = 0
    for value in values:
        s += value
    return s / len(values)


def avg_group(x):
    print_filtered_results(('all',))


def avg_sex_exp(x):
    print_filtered_results(('sex', 'experience'))


def print_filtered_results(field_set):
    grades = []
    exam = []
    for field in field_set:
        if field == 'sex':
            field_values = ('male', 'female')
        elif field == 'experience':
            field_values = (False, True)
        else:
            field_values = (None,)
        for field_value in field_values:
            for student in students:
                if student.get(field) == field_value:
                    grades.extend(student['grades'])
                    exam.append(student['exam'])
            print(const('AVG_GRADES'), const(field_value), ': {0:.1f}'.format(avg(grades)))
            print(const('AVG_EXAM'), const(field_value), ': {0:.1f}'.format(avg(exam)))
        print()


def best(x):
    titles = ['name', 'fname', 'grade']
    person = ['', '', 0]
    best_students = [dict(zip(titles, person)), ]
    for student in students:
        int_grade = 0.6 * avg(student['grades']) + 0.4 * student['exam']
        if int_grade < best_students[0]['grade']:
            continue
        if int_grade > best_students[0]['grade']:
            best_students.clear()
        best_students.append(dict(zip(titles, [student['name'], student['fname'], int_grade])))
    print(const('BEST_STUDENTS'), '\n')
    for student in best_students:
        print('{name} {fname} {grade:.1f}'.format(**student))


def hlp(description_list):
    for name, data in description_list.items():
        print(name, ': ', data['description'])


def command_selector(*arg):
    commands = {
        "a": {'description': 'average - средняя оценка по группе за домашки и за экзамен',
              'function': avg_group},
        "asx": {'description': 'average_sex_exp - средние оценки у мужчин и у женщин'
                           ' с опытом и без опыта программирования',
                'function': avg_sex_exp},
        "b": {'description': 'best student - студент или студенты с лучшей интегральной оценкой',
              'function': best},
        "h": {'description': 'help - список команд',
              'function': hlp}
    }
    print()
    input_com = commands.get(input(const('GET_COMMAND')))
    print()
    if input_com != None:
        input_com['function'](commands)
    else:
        print(const('NO_COMMAND'), '\n')


def main():
    students_generator()
    for student in students:
        print('{name:9}{experience:1} {grades} {exam}'.format(**student))
    while True:
        command_selector((avg_group, avg_sex_exp, best, hlp))


main()
