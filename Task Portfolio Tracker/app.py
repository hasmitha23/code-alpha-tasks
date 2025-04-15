from flask import Flask, render_template, request, redirect
import sqlite3

app = Flask(__name__)

# Initialize DB
def init_db():
    conn = sqlite3.connect('portfolio.db')
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS stocks (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    ticker TEXT NOT NULL,
                    shares INTEGER NOT NULL,
                    purchase_price REAL NOT NULL
                )''')
    conn.commit()
    conn.close()

@app.route('/')
def index():
    conn = sqlite3.connect('portfolio.db')
    c = conn.cursor()
    c.execute("SELECT * FROM stocks")
    stocks = c.fetchall()
    conn.close()
    return render_template('index.html', stocks=stocks)

@app.route('/add', methods=['POST'])
def add_stock():
    ticker = request.form['ticker']
    shares = int(request.form['shares'])
    price = float(request.form['price'])

    conn = sqlite3.connect('portfolio.db')
    c = conn.cursor()
    c.execute("INSERT INTO stocks (ticker, shares, purchase_price) VALUES (?, ?, ?)", (ticker, shares, price))
    conn.commit()
    conn.close()

    return redirect('/')

@app.route('/delete/<int:id>')
def delete_stock(id):
    conn = sqlite3.connect('portfolio.db')
    c = conn.cursor()
    c.execute("DELETE FROM stocks WHERE id = ?", (id,))
    conn.commit()
    conn.close()
    return redirect('/')

if __name__ == '__main__':
    init_db()
    app.run(debug=True)
