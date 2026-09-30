from flask import Flask, render_template, request, redirect, url_for, session
from database import init_db, get_all_items, get_stats

app = Flask(__name__)
app.secret_key = "ostrye_tupye_secret_key"

# Инициализация БД при запуске
init_db()

@app.route('/')
def index():
    if 'user' in session:
        return redirect(url_for('admin'))
    return redirect(url_for('login'))

@app.route('/login', methods=['GET', 'POST'])
def login():
    error = None
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        role = request.form.get('role')

        if username == 'admin' and password == 'admin123':
            session['user'] = username
            session['role'] = role
            return redirect(url_for('admin'))
        else:
            error = "Неверный логин или пароль!"

    return render_template('login.html', error=error)

@app.route('/admin')
def admin():
    if 'user' not in session:
        return redirect(url_for('login'))

    query = request.args.get('search', '')
    items = get_all_items(search_query=query if query else None)
    stats = get_stats()

    return render_template('admin.html', items=items, stats=stats, search_query=query)

@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('login'))

if __name__ == '__main__':
    app.run(debug=True, port=5000)
