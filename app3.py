from flask import Flask, render_template, request, redirect
import sqlite3

app = Flask(__name__)
DATABASE = 'database.db' # Ensure this matches your setup

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        name = request.form['name']
        email = request.form['email']
        phone = request.form['phone']

        with sqlite3.connect(DATABASE) as conn:
            cursor = conn.cursor()
            cursor.execute('INSERT INTO contacts (name, email, phone) VALUES (?, ?, ?)',
                           (name, email, phone))
            conn.commit()

        return redirect('/')

    with sqlite3.connect(DATABASE) as conn:
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM contacts')
        contacts = cursor.fetchall()

    return render_template('index.html', contacts=contacts)

# Function to create the table if it's missing
def init_db():
    with sqlite3.connect(DATABASE) as conn:
        conn.execute('''
            CREATE TABLE IF NOT EXISTS contacts 
            (id INTEGER PRIMARY KEY AUTOINCREMENT, 
             name TEXT, email TEXT, phone TEXT)
        ''')
        conn.commit()

if __name__ == '__main__':
    init_db()  # This MUST run to create the 'contacts' table
    app.run(host="0.0.0.0", port=8001, debug=True)