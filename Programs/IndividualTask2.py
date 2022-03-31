#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import pandas as pd
import json
from jsonschema import validate
from pathlib import Path
import click
import argparse


FILE_NAME = 'json_file.json'
SETTINGS_FILE = 'settings.json'


def add_element(name, num, tm):
    trains = {}
    trains['name'] = name
    trains['num'] = int(num)
    trains['tm'] = tm
    schema = ''
    with open('schema.json', 'r') as f:
        schema = json.loads(f.read())
    validate(instance=trains, schema=schema)
    with open(FILE_NAME, 'a') as f:
        f.write(json.dumps(trains) + '\n')


def find_train(num):
    with open('json_file.json', 'r') as f:
        trains = f.readlines()
        for dcts in trains:
            dcts = json.loads(dcts)
            if dcts['num'] == int(num):
                click.echo(
                    f'Конечный пункт: {dcts["name"]} \n'
                    f'Номер поезда: {dcts["num"]} \n'
                    f'Время отправления: {(dcts["tm"])}'
                )
                return
        click.echo('Поезда с таким номером нет')


def main(command_line=None):
    file_parser = argparse.ArgumentParser(add_help=False)
    file_parser.add_argument(
        "filename",
        action="store",
        help="Имя файла для хранения данных"
    )
    parser = argparse.ArgumentParser("trains")
    parser.add_argument(
        "--version",
        action="version",
        version="%(prog)s 0.1.0"
    )
    subparsers = parser.add_subparsers(dest="command")
    add = subparsers.add_parser(
        "add",
        parents=[file_parser],
        help="Добавить новое отправление"
    )
    add.add_argument(
        "-trd",
        "--train_dest",
        action="store",
        required=True,
        help="Пункт назначения поезда"
    )
    add.add_argument(
        "-n",
        "--number",
        action="store",
        help="Номер поезда"
    )
    add.add_argument(
        "-t",
        "--time",
        action="store",
        required=True,
        help="Время отправления поезда"
    )
    select = subparsers.add_parser(
        "select",
        parents=[file_parser],
        help="Выбрать поезда по номеру"
    )
    select.add_argument(
        "-n",
        "--number",
        action="store",
        required=True,
        help="Номер поезда"
    )
    args = parser.parse_args(command_line)
    try:
        if args.command == "add":
            add_element(
                args.train_dest,
                args.number,
                args.time
            )
        elif args.command == "find":
            find_train(args.number)
    except Exception as e:
        print(e)


if __name__ == '__main__':
    print('LOADING...')
    with open(SETTINGS_FILE, 'r') as f:
        settings = json.loads(f.read())
        if settings['gitignore'] == False:
            path = Path(__file__).resolve()
            print(path.parents[1])
            par_path = path.parents[1]
            with open(str(par_path) + '\\.gitignore', 'a') as gig:
                gig.write('\n' + '*.json' + '\n')
    with open(SETTINGS_FILE, 'w') as f:
        f.write(json.dumps({'gitignore': True}))

    print('Hello!')
    flag = True
    while flag:
        main()
        """
        print('1. Добавить новый поезд')
        print('2. Вывести информацию о поезде')
        print('3.Выход из программы')
        com = int(input('введите номер команды: '))
        if com == 1:
            add_element()
        elif com == 2:
            train_num = input('Введите номер поезда: ')
            find_train(train_num)
        elif com == 3:
            flag = False
        """
