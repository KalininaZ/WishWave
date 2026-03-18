import sqlite3
from flask import Flask, render_template, request, redirect

app = Flask(__name__)

def get_db_connection():
    conn = sqlite3.connect('wishlist.db')
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    conn = get_db_connection()
    # Добавили поле image_url
    conn.execute('''
        CREATE TABLE IF NOT EXISTS wishes (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            price TEXT,
            link TEXT,
            description TEXT,
            status TEXT,
            image_url TEXT
        )
    ''')
    conn.commit()
    conn.close()

@app.route('/', methods=['GET', 'POST'])
def index():
    conn = get_db_connection()
    if request.method == 'POST':
        name = request.form['name']
        try:
            price = int(request.form['price'])
        except:
            price = 0
        link = request.form['link']
        desc = request.form['description']
        status = request.form['status']
        image_url = request.form['image_url'] # Получаем ссылку на фото

        conn.execute('INSERT INTO wishes (name, price, link, description, status, image_url) VALUES (?, ?, ?, ?, ?, ?)',
                     (name, price, link, desc, status, image_url))
        conn.commit()
        return redirect('/')

    items = conn.execute('SELECT * FROM wishes ORDER BY id DESC').fetchall()
    conn.close()
    return render_template('index.html', wishes=items)

@app.route('/delete/<int:id>')
def delete(id):
    conn = get_db_connection()
    conn.execute('DELETE FROM wishes WHERE id = ?', (id,))
    conn.commit()
    conn.close()
    return redirect('/')

@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404

@app.route('/update_status/<int:id>', methods=['POST'])
def update_status(id):
    new_status = request.form.get('status')
    conn = get_db_connection()
    conn.execute('UPDATE wishes SET status = ? WHERE id = ?', (new_status, id))
    conn.commit()
    conn.close()
    return redirect('/')

if __name__ == '__main__':
    init_db()
    app.run(debug=True)