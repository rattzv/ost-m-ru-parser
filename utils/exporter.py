import json
import os
import sqlite3

from utils.utils import get_requests, print_template


FILENAME = "ost-m-ru"


def download_price_list(url, reports_folder, second_city):
    try:
        if second_city:
            price_list_path = os.path.join(reports_folder, f'price-list-{FILENAME}.xlsx')
        else:
            price_list_path = os.path.join(reports_folder, f'price-list-ost-ya-ru.xlsx')

        response = get_requests(url)
        if response is False:
            return False

        with open(price_list_path, "wb") as temp_file:
            temp_file.write(response.content)
        return price_list_path
    except:
        return False


def remove_old_data(reports_folder):
    report_file_sqlite = os.path.join(reports_folder, 'sqlite', f'{FILENAME}.sqlite')
    report_file_json = os.path.join(reports_folder, 'sqlite', f'{FILENAME}.json')
    report_file_all_json = os.path.join(reports_folder, 'products.json')
    try:
        if os.path.exists(report_file_sqlite):
            print_template(f"Remove old data {report_file_sqlite}...")
            os.remove(report_file_sqlite)
        if os.path.exists(report_file_json):
            print_template(f"Remove old data {report_file_json}...")
            os.remove(report_file_json)
        if os.path.exists(report_file_all_json):
            print_template(f"Remove old data {report_file_all_json}...")
            os.remove(report_file_all_json)
    except Exception as ex:
        print(print_template(f'Error: {ex}'))


def save_to_sqlite(products, reports_folder):
    try:
        report_file = os.path.join(reports_folder, 'sqlite', FILENAME)

        conn = sqlite3.connect(report_file + ".sqlite")
        cursor = conn.cursor()
        cursor.execute('''CREATE TABLE IF NOT EXISTS json_data (id INTEGER PRIMARY KEY, data TEXT UNIQUE)''')

        for product in products:
            try:
                data = json.dumps(product, ensure_ascii=False, indent=4)
                cursor.execute("INSERT OR IGNORE INTO json_data (data) VALUES (?)", (data,))
            except:
                continue
        conn.commit()
    except Exception as ex:
        print(print_template(f'Error: {ex}'))
        return False


def convert_to_json(reports_folder):
    try:
        sqlite_report_file = os.path.join(reports_folder, 'sqlite', f'{FILENAME}.sqlite')
        if not os.path.exists(sqlite_report_file):
            return False

        conn = sqlite3.connect(sqlite_report_file)
        cursor = conn.cursor()
        cursor.execute("SELECT data FROM json_data")
        rows = cursor.fetchall()
        conn.close()

        data_list = []
        for row in rows:
            try:
                data_list.append(json.loads(row[0]))
            except:
                continue

        print_template(f"Convert to json {sqlite_report_file}...")

        total_report_file = os.path.join(reports_folder, 'products.json')
        with open(total_report_file, 'w', encoding="utf-8") as file:
            json.dump(data_list, file, ensure_ascii=False, indent=4)
        return len(data_list)
    except Exception as ex:
        print(print_template(f'Error: {ex}'))
        return False





