import sqlite3
from flask import Flask, jsonify

app = Flask(__name__)

@app.route('/')
def index():
    return 'Profitto Full Stack'

@app.route('/universitas')
def universitas():
    con = sqlite3.connect('universitas.sqlite3')
    cur = con.cursor()

    # Get data universitas, domains, dan web_pages
    cur.execute('SELECT * FROM universitas')
    universitas = cur.fetchall()
    cur.execute('SELECT * FROM web_pages')
    domains = cur.fetchall()
    cur.execute('SELECT * FROM domains')
    web_pages = cur.fetchall()

    data = []
    for univ in universitas:
        temp_data = {
            'id': univ[0],
            'alpha_two_code': univ[1],
            'country': univ[2],
            'name': univ[3],
            'state_province': univ[4],
            'domains': [],
            'web_pages': []
        }

        for domain in domains:
            if domain[2] == univ[0]:
                temp_data['domains'].append(domain[1])

        for web_page in web_pages:
            if web_page[2] == univ[0]:
                temp_data['web_pages'].append(web_page[1])

        data.append(temp_data)

    con.commit()
    con.close()

    return jsonify({'message': 'success', 'count_data': len(data), 'data': data})

if __name__ == '__main__':
    app.run(debug=True)