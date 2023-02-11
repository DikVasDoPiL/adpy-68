import re
from pprint import pprint
# читаем адресную книгу в формате CSV в список contacts_list
import csv
with open("phonebook_raw.csv", 'r', encoding='utf-8') as f:
    rows = csv.reader(f, delimiter=",")
    contacts_list = list(rows)

# Буду использовать промежуточный словарь для отслеживания дубликатов записи,
# т.к. нет явного ключа, считаю, что нет людей с одинаковыми ФИО
# отслеживание по связке ФИО, пустые поля существующей записи будут обновляться
new_list = {}

# 1. поместить Фамилию, Имя и Отчество человека в поля lastname,
#    firstname и surname соответственно.
#    В записной книжке изначально может быть Ф + ИО, ФИО, а может быть сразу правильно: Ф+И+О

# перебираю записи в общем списке без заголовка
for contact in contacts_list[1:]:

    # для начала поймаю связку ФИО в кортеж фиксированной длины
    string = ','.join(contact)
    fio_pattern_old = re.compile(r'([А-Я]\w*)?\W([А-Я]\w*)?\W([А-Я]\w*)?\W')
    fio_new = fio_pattern_old.findall(string)[0]

# 2. привести все телефоны в формат +7(999)999-99-99.
#    Если есть добавочный номер, формат будет такой: +7(999)999-99-99 доб.9999;

# телефон нахожу через группировку, с проверкой условия наличия добавочного номера, опять же через кортеж
    phone_pattern_old = re.compile(
        r'(\+7|8).*?(\d{3}).*?(\d{3}).*?(\d{2}).*?(\d{2})(.+доб\..)?(\d{3,4})?(.,)?')
    pn = phone_pattern_old.findall(string)
    if len(pn) > 0:
        raw_phone = '+7(' + pn[0][1] + ')' + pn[0][2] + \
            '-' + pn[0][3] + '-' + pn[0][4]
        if len(pn[0][6]) > 0:
            phone_ext = ' доб.' + pn[0][6]
        else:
            phone_ext = ''

        new_phone = raw_phone + phone_ext
    else:
        new_phone = ''

# здесь подготавливаю запись в промежуточный словарь контактов
    lastname = fio_new[0]
    firstname = fio_new[1]
    surname = fio_new[2]
    organization = contact[3]
    position = contact[4]
    phone = new_phone
    email = contact[6]
    new_string = [lastname, firstname, surname,
                  organization, position, phone, email]

# 3. объединить все дублирующиеся записи о человеке в одну.

# проверяю через False есть ли ФИО ключ в словаре. если да, то дополняю запись.
    temp_key = fio_new[:1]
    if temp_key not in new_list.keys():
        new_list[temp_key] = new_string
    else:
        ts = new_list[temp_key]
        if not ts[0]:
            ts[0] = lastname
        if not ts[1]:
            ts[1] = firstname
        if not ts[2]:
            ts[2] = surname
        if not ts[3]:
            ts[3] = organization
        if not ts[4]:
            ts[4] = position
        if not ts[5]:
            ts[5] = phone
        if not ts[6]:
            ts[6] = email

# подготавливаю csv
new_adressbook = [contacts_list[0]]
for i in new_list.values():
    new_adressbook.append(i)

# pprint(contacts_list)
pprint(new_adressbook)
pprint('Job Done')
with open("phonebook.csv", "w", encoding='utf-8', newline='') as f:
    datawriter = csv.writer(f, delimiter=',')
    # Вместо contacts_list подставьте свой список
    datawriter.writerows(new_adressbook)
