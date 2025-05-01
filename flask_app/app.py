from flask import Flask, render_template, request, redirect, url_for
import sqlite3

app = Flask(__name__)

# إنشاء قاعدة البيانات
def init_db():
    with sqlite3.connect("data.db") as conn:
        conn.execute('''
            CREATE TABLE IF NOT EXISTS entries (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                category TEXT,
                section TEXT,
                content TEXT,
                notes TEXT,
                price REAL
            )
        ''')

@app.route('/')
def index():
    with sqlite3.connect("data.db") as conn:
        entries = conn.execute("SELECT * FROM entries").fetchall()
        categories = {}
        total = 0
        for entry in entries:
            cat = entry[1]
            price = entry[5]
            categories.setdefault(cat, []).append(entry)
            total += price
        category_totals = {k: sum(e[5] for e in v) for k, v in categories.items()}
    return render_template('index.html', categories=categories, totals=category_totals, grand_total=total)

@app.route('/add', methods=['POST'])
def add():
    category = request.form['category']
    section = request.form['section']
    content = request.form['content']
    notes = request.form['notes']
    price = float(request.form['price'])

    with sqlite3.connect("data.db") as conn:
        conn.execute("INSERT INTO entries (category, section, content, notes, price) VALUES (?, ?, ?, ?, ?)",
                     (category, section, content, notes, price))
    return redirect(url_for('index'))

if __name__ == '__main__':
    init_db()
    app.run(debug=True)
