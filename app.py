from flask import Flask, render_template, request, redirect
import sqlite3

app = Flask(__name__)

# Initialize the database
def init_db():
    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS submissions (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            message TEXT NOT NULL
        )
    ''')
    conn.commit()
    conn.close()

# Home route with form
@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        name = request.form['name']
        message = request.form['message']
        
        conn = sqlite3.connect('database.db')
        cursor = conn.cursor()
        cursor.execute("INSERT INTO submissions (name, message) VALUES (?, ?)", (name, message))
        conn.commit()
        conn.close()
        
        return redirect('/submissions')

    return render_template('index.html')

# Show all submitted messages
@app.route('/submissions')
def submissions():
    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()
    cursor.execute("SELECT name, message FROM submissions")
    data = cursor.fetchall()
    conn.close()
    return render_template('submissions.html', data=data)

if __name__ == '__main__':
    init_db()
    app.run(debug=True)
