import sqlite3
import requests

class Model():
    def create_table(self):
        con = sqlite3.connect('universitas.sqlite3')
        cur = con.cursor()

        cur.execute('CREATE TABLE IF NOT EXISTS universitas (id INTEGER PRIMARY KEY, alpha_two_code CHAR(12), country VARCHAR(55), name VARCHAR(55), state_province VARCHAR(55))')
        cur.execute('CREATE TABLE IF NOT EXISTS domains (id INTEGER PRIMARY KEY, domain VARCHAR(55), universitas_id INTEGER, FOREIGN KEY (universitas_id) REFERENCES universitas (id))')
        cur.execute('CREATE TABLE IF NOT EXISTS web_pages (id INTEGER PRIMARY KEY, web_page VARCHAR(55), universitas_id INTEGER, FOREIGN KEY (universitas_id) REFERENCES universitas (id))')
        
        con.commit()
        con.close()

    # Hanya jalankan sekali saja untuk memindahkan data dari API ke database
    def store_data_from_api(self):
        con = sqlite3.connect('universitas.sqlite3')
        cur = con.cursor()

        url = 'https://test-profitto-api.s3.ap-southeast-1.amazonaws.com/university.json'
        response = requests.get(url)
        universitass = response.json()

        for universitas in universitass:
            cur.execute('INSERT INTO universitas (alpha_two_code, country, name, state_province) VALUES (?, ?, ?, ?)', (universitas['alpha_two_code'], universitas['country'], universitas['name'], universitas['state-province']))
            id_universitas = cur.lastrowid

            for domain in universitas['domains']:
                cur.execute('INSERT INTO domains (domain, universitas_id) VALUES (?, ?)', (domain, id_universitas))

            for web_page in universitas['web_pages']:
                cur.execute('INSERT INTO web_pages (web_page, universitas_id) VALUES (?, ?)', (web_page, id_universitas))

        con.commit()
        con.close()

model = Model()
model.create_table()
model.store_data_from_api()