import dash
from dash import dcc, html
from dash.dependencies import Input, Output
import dash_auth
from flask import session
import time
import dash_bootstrap_components as dbc

# Список пользователей и паролей для BasicAuth
VALID_USERNAME_PASSWORD_PAIRS = {
    'user1': 'password1',
    'user2': 'password2'
}

# Время действия сессии (в секундах)
SESSION_TIMEOUT = 15 * 60  # 15 минут

# Инициализация Dash приложения
app = dash.Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])

# Настройка авторизации
auth = dash_auth.BasicAuth(
    app,
    VALID_USERNAME_PASSWORD_PAIRS
)

# Разметка страницы входа
login_layout = html.Div([
    dbc.Container([
        dbc.Row([dbc.Col(html.H2("Login"), width=12)]),
        dbc.Row([dbc.Col(dbc.Input(id='username', placeholder='Username', type='text'), width=12)]),
        dbc.Row([dbc.Col(dbc.Input(id='password', placeholder='Password', type='password'), width=12)]),
        dbc.Row([dbc.Col(dbc.Button('Login', id='login-button', color='primary', block=True), width=12)]),
        dbc.Row([dbc.Col(html.Div(id='login-message', style={'color': 'red'}), width=12)])
    ])
])

# Разметка страницы с приветствием
welcome_layout = html.Div([
    html.H1('Welcome to the Dashboard'),
    html.Button('Log Out', id='logout-button', n_clicks=0),
    html.Div(id='user-info')
])

# Логика перехода на страницу входа и выхода
@app.callback(
    Output('user-info', 'children'),
    Output('logout-button', 'style'),
    Input('logout-button', 'n_clicks'),
    prevent_initial_call=True
)
def handle_logout(n_clicks):
    if n_clicks > 0:
        session.clear()  # Очистить сессию
        return '', {'display': 'none'}  # Скрыть кнопку выхода
    return 'You are logged in.', {'display': 'block'}

@app.callback(
    Output('login-message', 'children'),
    Output('url', 'pathname'),
    Input('login-button', 'n_clicks'),
    Input('username', 'value'),
    Input('password', 'value'),
    prevent_initial_call=True
)
def login(n_clicks, username, password):
    if n_clicks > 0:
        if username in VALID_USERNAME_PASSWORD_PAIRS and VALID_USERNAME_PASSWORD_PAIRS[username] == password:
            session['logged_in'] = True  # Сохраняем состояние в сессии
            session['last_activity'] = time.time()  # Сохраняем время последней активности
            return '', '/welcome'  # Переходим на страницу приветствия
        else:
            return 'Invalid credentials, please try again.', '/login'  # Сообщение об ошибке
    return '', '/login'

# Проверка времени последней активности
@app.callback(
    Output('page-content', 'children'),
    Input('url', 'pathname')
)
def display_page(pathname):
    # Проверяем, если сессия истекла
    if 'logged_in' in session and 'last_activity' in session:
        time_since_last_activity = time.time() - session['last_activity']
        if time_since_last_activity > SESSION_TIMEOUT:
            session.clear()  # Очищаем сессию
            return login_layout  # Перенаправляем на страницу входа
        session['last_activity'] = time.time()  # Обновляем время последней активности

    if pathname == '/welcome':
        return welcome_layout
    else:
        return login_layout

# Определение основной разметки
app.layout = html.Div([
    dcc.Location(id='url', refresh=False),
    html.Div(id='page-content')
])

if __name__ == '__main__':
    app.run_server(debug=True)
