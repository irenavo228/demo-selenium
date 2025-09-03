import csv
import json
import xml.etree.ElementTree as ET
import subprocess
from pathlib import Path
from datetime import datetime


def handle_none(value):
    return None if value == "null" else value


def read_sql(file_path):
    with open(file_path, 'r') as file:
        return file.read()


def read_csv(file_path):
    with open(file_path, mode='r', encoding='utf-8') as file:
        reader = csv.DictReader(file)
        data = [row for row in reader]
        sorted_data = sorted(data, key=lambda x: int(x['no']))
        return sorted_data


def read_json(file_path):
    with open(file_path, 'r', encoding='utf-8') as file:
        data = json.load(file)
        for item in data:
            yield item


def read_xml(file_path):
    tree = ET.parse(file_path)
    root = tree.getroot()

    for element in root.iter():
        attributes = element.attrib
        if attributes:
            yield {'tag': element.tag, 'attributes': attributes}


def read_txt(file_path):
    with open(file_path, 'r', encoding='utf-8') as file:
        for line in file:
            values = line.split()
            yield values


def gen_report():
    subprocess.run(['allure', 'serve', 'allure-results'])


def get_full_path(relative_path):
    base_dir = Path(__file__).resolve().parent.parent
    full_path = base_dir / relative_path
    return full_path.resolve()


def col_to_letter(col_index):
    letter = ""
    while col_index > 0:
        col_index, remainder = divmod(col_index - 1, 26)
        letter = chr(65 + remainder) + letter
    return letter


def load_config(relative_path, env):
    full_path = get_full_path(relative_path)
    with open(full_path, 'r', encoding='utf-8') as file:
        data = json.load(file)
        return data.get(env, {})