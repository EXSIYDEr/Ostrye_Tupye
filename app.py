from flask import Flask, render_template, request, redirect, url_for, session
from database import init_db, get_all_items, get_stats, add_item_to_db, get_all_item_names, issue_item, get_issue_history, get_low_stock_items, get_reports_stats

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

        if username == 'admin' and password == 'admin12345':
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

@app.route('/issues', methods=['GET', 'POST'])
def issues():
    if 'user' not in session:
        return redirect(url_for('login'))

    message = None
    error = None

    if request.method == 'POST':
        item_id = int(request.form.get('item_id'))
        issue_qty = int(request.form.get('quantity', 0))
        reason = request.form.get('reason')
        # В реальной программе берется из session, но для проекта №21 укажем заглушку
        worker_name = session.get('user', 'Неизвестный работник')

        if issue_qty <= 0:
            error = "Количество должно быть больше нуля."
        else:
            success, msg = issue_item(item_id, issue_qty, reason, worker_name)
            if success:
                message = msg
            else:
                error = msg

    # Получаем данные для отрисовки страницы: товары для списка и историю
    available_items = get_all_item_names()
    history = get_issue_history()

    return render_template('issues.html', items=available_items, history=history, message=message, error=error)


@app.route('/reports')
def reports():
    if 'user' not in session:
        return redirect(url_for('login'))

    # Получаем данные из базы
    low_stock = get_low_stock_items()
    stats = get_reports_stats()

    return render_template('reports.html', low_stock=low_stock, stats=stats)


@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('login'))

@app.route('/manage_items', methods=['GET', 'POST'])
def manage_items():
    if 'user' not in session:
        return redirect(url_for('login'))

    message = None
    if request.method == 'POST':
        # Получаем данные из формы добавления товара
        name = request.form.get('name')
        category = request.form.get('category')
        unit = request.form.get('unit')
        quantity = int(request.form.get('quantity', 0))
        min_limit = int(request.form.get('min_limit', 0))
        storage_place = request.form.get('storage_place')

        # Обращаемся к классу хранилища для сохранения
        add_item_to_db(name, category, unit, quantity, min_limit, storage_place)
        message = f"Товар «{name}» успешно добавлен на склад!"

    return render_template('manage_items.html', message=message)

if __name__ == '__main__':
    app.run(debug=True, port=5000)
