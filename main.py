import os
from django.conf import settings

BASE_DIR = os.path.dirname(__file__)

settings.configure(
    DEBUG=True,
    SECRET_KEY='chave',
    ROOT_URLCONF=__name__,
    ALLOWED_HOSTS=['*'],
    MIDDLEWARE=[
        'django.middleware.common.CommonMiddleware',
        'django.middleware.csrf.CsrfViewMiddleware',
        'django.contrib.sessions.middleware.SessionMiddleware',
        'django.contrib.auth.middleware.AuthenticationMiddleware',
    ],
    INSTALLED_APPS=[
        'django.contrib.contenttypes',
        'django.contrib.auth',
        'django.contrib.sessions',
    ],
    DATABASES={
        'default': {
            'ENGINE': 'django.db.backends.sqlite3',
            'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
        }
    },
)

import django
django.setup()

# Criar as tabelas do banco de dados
from django.core.management import call_command
call_command('migrate', '--run-syncdb', verbosity=0)

from django.urls import path
from django.http import HttpResponse
from django.shortcuts import redirect
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.middleware.csrf import get_token

# ================= HTML =================

def tela(request, erro="", sucesso=""):
    csrf = get_token(request)

    return f"""
<!DOCTYPE html>
<html>
<head>
<meta charset="UTF-8">
<title>Login</title>

<style>
* {{
    margin: 0;
    padding: 0;
    box-sizing: border-box;
    font-family: Arial;
}}

body {{
    height: 100vh;
    background: #e8f4f8;
    display: flex;
    justify-content: center;
    align-items: center;
    position: relative;
}}

.developer {{
    position: fixed;
    bottom: 20px;
    right: 20px;
    color: #1e40af;
    font-size: 12px;
    font-style: italic;
    opacity: 0.7;
}}

.container {{
    width: 800px;
    height: 500px;
    background: white;
    border-radius: 20px;
    display: flex;
    overflow: hidden;
    box-shadow: 0 10px 30px rgba(30, 64, 175, 0.3);
}}

.left {{
    width: 50%;
    background: linear-gradient(135deg, #1e40af 0%, #3b82f6 100%);
    color: white;
    display: flex;
    flex-direction: column;
    justify-content: center;
    align-items: center;
    padding: 40px;
}}

.left h1 {{
    font-size: 32px;
    margin-bottom: 10px;
}}

.left p {{
    margin-bottom: 10px;
    font-size: 16px;
}}

.left button {{
    margin-top: 20px;
    padding: 12px 35px;
    border-radius: 25px;
    border: 2px solid white;
    background: transparent;
    color: white;
    cursor: pointer;
    font-weight: bold;
    transition: all 0.3s;
}}

.left button:hover {{
    background: white;
    color: #1e40af;
}}

.right {{
    width: 50%;
    display: flex;
    justify-content: center;
    align-items: center;
}}

.form {{
    width: 80%;
}}

.form h2 {{
    margin-bottom: 20px;
    color: #1e40af;
}}

.input-box {{
    margin-bottom: 15px;
}}

.input-box input {{
    width: 100%;
    padding: 12px;
    border: 2px solid #e5e7eb;
    background: #f9fafb;
    border-radius: 8px;
    transition: all 0.3s;
}}

.input-box input:focus {{
    outline: none;
    border-color: #3b82f6;
    background: white;
}}

.submit {{
    width: 100%;
    padding: 12px;
    background: linear-gradient(135deg, #1e40af 0%, #3b82f6 100%);
    border: none;
    border-radius: 25px;
    color: white;
    cursor: pointer;
    font-weight: bold;
    transition: all 0.3s;
}}

.submit:hover {{
    transform: translateY(-2px);
    box-shadow: 0 5px 15px rgba(30, 64, 175, 0.3);
}}

#cadastro {{
    display: none;
}}

.erro {{
    color: #dc2626;
    margin-top: 10px;
    font-size: 14px;
    padding: 8px;
    border-radius: 5px;
    background: #fee2e2;
}}

.sucesso {{
    color: #16a34a;
    margin-top: 10px;
    font-size: 14px;
    padding: 8px;
    border-radius: 5px;
    background: #dcfce7;
}}
</style>

</head>

<body>

<div class="developer">Desenvolvido por Anna Dev</div>

<div class="container">

    <div class="left">
        <h1>Bem-vindo de Volta!</h1>
        <p>Entre na sua conta ou crie uma nova</p>
        <button onclick="mostrarLogin()">ENTRAR</button>
        <button onclick="mostrarCadastro()">CADASTRAR</button>
    </div>

    <div class="right">

        <!-- LOGIN -->
        <form method="POST" action="/login" id="login" class="form">
            <input type="hidden" name="csrfmiddlewaretoken" value="{csrf}">
            <h2>Login</h2>
            <div class="input-box">
                <input name="username" placeholder="Usuário" required>
            </div>
            <div class="input-box">
                <input type="password" name="password" placeholder="Senha" required>
            </div>
            <button class="submit">Entrar</button>
            {f'<div class="erro">{erro}</div>' if erro else ''}
            {f'<div class="sucesso">{sucesso}</div>' if sucesso else ''}
        </form>

        <!-- CADASTRO -->
        <form method="POST" action="/cadastro" id="cadastro" class="form">
            <input type="hidden" name="csrfmiddlewaretoken" value="{csrf}">
            <h2>Criar Conta</h2>
            <div class="input-box">
                <input name="username" placeholder="Usuário" required>
            </div>
            <div class="input-box">
                <input type="password" name="password" placeholder="Senha" required>
            </div>
            <button class="submit">Cadastrar</button>
        </form>

    </div>

</div>

<script>
function mostrarLogin() {{
    document.getElementById("login").style.display = "block";
    document.getElementById("cadastro").style.display = "none";
}}

function mostrarCadastro() {{
    document.getElementById("login").style.display = "none";
    document.getElementById("cadastro").style.display = "block";
}}
</script>

</body>
</html>
"""

def dashboard_html(user):
    return f"""
    <html>
    <body style="background:#1e3a8a;color:white;font-family:Arial;padding:40px">
        <h1>Dashboard</h1>
        <p>Bem-vindo(a), {user}</p>
        <a href="/logout" style="color:#60a5fa;text-decoration:none">Sair</a>
    </body>
    </html>
    """

# ================= VIEWS =================

def home(request):
    return HttpResponse(tela(request))

def login_view(request):
    if request.method == "POST":
        user = request.POST.get("username")
        senha = request.POST.get("password")

        usuario = authenticate(request, username=user, password=senha)

        if usuario:
            login(request, usuario)
            return redirect("/dashboard")
        else:
            return HttpResponse(tela(request, erro="Login inválido"))

    return redirect("/")

def cadastro_view(request):
    if request.method == "POST":
        user = request.POST.get("username")
        senha = request.POST.get("password")

        if User.objects.filter(username=user).exists():
            return HttpResponse(tela(request, erro="Usuário já existe"))

        User.objects.create_user(username=user, password=senha)
        return HttpResponse(tela(request, sucesso="Cadastro realizado com sucesso! Faça login."))

    return redirect("/")

def dashboard(request):
    if not request.user.is_authenticated:
        return redirect("/")
    return HttpResponse(dashboard_html(request.user.username))

def logout_view(request):
    logout(request)
    return redirect("/")

# ================= URLS =================

urlpatterns = [
    path('', home),
    path('login', login_view),
    path('cadastro', cadastro_view),
    path('dashboard', dashboard),
    path('logout', logout_view),
]

# ================= RUN =================

from django.core.management import execute_from_command_line

if __name__ == "__main__":
    execute_from_command_line(["manage.py", "runserver"])