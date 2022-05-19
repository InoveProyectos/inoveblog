import os
import json
import random
import string
import requests
import time
from datetime import datetime

import traceback
from flask import Flask, request, make_response, jsonify, render_template, Response, redirect, url_for

def get_env_variable(name):
    try:
        return os.environ[name]
    except KeyError:
        message = "Expected environment variable '{}' not set.".format(name)
        raise Exception(message)

# Cargar variables de entorno definidas (si es que hay)
from dotenv import load_dotenv
load_dotenv()

# Crear el server Flask
app = Flask(__name__)

# Clave que utilizaremos para encriptar los datos
app.secret_key = "flask_session_key_inventada"

# Cors
from flask_cors import CORS, cross_origin
CORS(app)

# Base de datos
from flask_login import UserMixin
from flask_sqlalchemy import SQLAlchemy
#app.config["SQLALCHEMY_DATABASE_URI"] = f"sqlite:///inoveblog.db"
app.config["SQLALCHEMY_DATABASE_URI"] = get_env_variable("DATABASE_URL")
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy()
db.init_app(app)

class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50))
    apikey = db.Column(db.String(50))


class Post(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    titulo = db.Column(db.String(100))
    texto = db.Column(db.String(300))

    user_id = db.Column(db.Integer, db.ForeignKey("user.id"))

    user = db.relationship("User")

# Configurar el sistema de login
from flask_login import LoginManager, login_user, logout_user, login_required, current_user
login_manager = LoginManager()
login_manager.login_view = 'login'
login_manager.init_app(app)

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

APP_ROOT = os.path.dirname(os.path.abspath(__file__))
UPLOAD_FOLDER = os.path.join(APP_ROOT, "static", "upload")
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

LOGIN_PASSWORD = "inovejs"

# ------------ Views ----------------- #

@app.route('/login')
def login():
    return render_template('login.html')

@app.route('/logout')
@login_required
def logout():
    # Deslogarse
    logout_user()
    return redirect(url_for('login'))

@app.route("/")
@login_required
def blog():
    try:
        usuario = current_user.name
        if os.path.exists(os.path.join(UPLOAD_FOLDER, f"{usuario}.png")) == True:
            foto = url_for('static', filename=f'upload/{usuario}.png')
        else:
            foto = url_for('static', filename=f'images/avatar_icon.png')
        foto += f"?v={int(time.time())}"
        return render_template('blog.html', usuario=usuario, foto=foto, apikey=current_user.apikey)
    except Exception as e:
        print(e)
        print(jsonify({'trace': traceback.format_exc()}))
        return Response(status=400)

# Referencia:
# https://swagger.io/specification/
@app.route('/docs')
def docs():
    return render_template('swaggerui.html')

# ---------------- API ------------------------

@app.route('/api/v1.0/login', methods=['POST'])
@cross_origin(origin='*', headers=['Content-Type','Authorization'])
def api_login():
    try:
        # Validate request data format
        content_type = request.headers.get('Content-Type')
        if ('application/x-www-form-urlencoded' not in content_type and
            'multipart/form-data' not in content_type ):
            return Response(status=415)

        # Read data
        usuario = request.form['usuario']
        password = request.form['password']

        # Process request
        if password != LOGIN_PASSWORD:
            print("LOGIN_PASSWORD incorrect")
            return Response(status=401)

        url = "http://23.92.69.190/administracion/usuarios/exists/"
        payload = {"username": usuario}
        res = requests.post(url, data=json.dumps(payload), headers={"Content-Type":"application/json"})
        if res.status_code != 200:
            print("USER incorrect")
            return Response(status=401)

        user = User.query.filter_by(name=usuario).first()
        # Si el usuario existe no puedo crearlo
        if user is None:
            # Crear password
            # https://pynative.com/python-generate-random-string/
            #characters = string.ascii_lowercase + string.digits + string.punctuation
            characters = string.ascii_lowercase + string.digits
            apikey = ''.join(random.choice(characters) for i in range(8))
            user = User(name=usuario, apikey=apikey)
            # agregar usuario a la base de datos
            db.session.add(user)
            db.session.commit()

        print("login success of user", user.name)
        login_user(user)
        return make_response(jsonify({"apikey": user.apikey}), 200)

    except Exception as e:
        print(e)
        print(jsonify({'trace': traceback.format_exc()}))
        return Response(status=401)


@app.route('/api/v1.0/post', methods=['GET', 'POST', 'DELETE'])
@cross_origin(origin='*', headers=['Content-Type','Authorization'])
def post():
    try:
        if request.method == 'GET':
            usuario = request.args.get('usuario')
            apikey = request.args.get('apikey')

            if usuario is None or apikey is None:
                return Response(status=401)

            user = User.query.filter_by(name=usuario).first()
            if user is None or user.apikey != apikey:
                # Si el usuario no existe o la apikey es invalida salgo
                return Response(status=401)
    
            posts = []
            for post in Post.query.filter_by(user=user).order_by(Post.id.desc()).limit(3):
                posts.append({"titulo": post.titulo, "texto": post.texto})
            return make_response(jsonify({"posts": posts}), 200)

        if request.method == 'POST':
            # Validate request data format
            content_type = request.headers.get('Content-Type')
            if 'application/json' not in content_type:
                return Response(status=415)

            usuario = request.json['usuario']
            apikey = request.json['apikey']
            titulo = request.json['titulo']
            texto = request.json['texto']

            user = User.query.filter_by(name=usuario).first()
            if user is None or user.apikey != apikey:
                # Si el usuario no existe o la apikey es invalida salgo
                return Response(status=401)

            post = Post(user=user, titulo=titulo, texto=texto)
            # agregar post a la base de datos
            db.session.add(post)
            db.session.commit()

            return make_response(jsonify({"id": post.id, "titulo": post.titulo, "texto": post.texto}), 200)

        if request.method == 'DELETE':
            # Validate request data format
            content_type = request.headers.get('Content-Type')
            if 'application/json' not in content_type:
                return Response(status=415)

            usuario = request.json['usuario']
            apikey = request.json['apikey']

            user = User.query.filter_by(name=usuario).first()
            if user is None or user.apikey != apikey:
                # Si el usuario no existe o la apikey es invalida salgo
                return Response(status=401)

            posts = Post.query.filter_by(user=user)
            posts.delete()
            db.session.commit()

            return Response(status=200)
    except Exception as e:
        print(e)
        print(jsonify({'trace': traceback.format_exc()}))
        return Response(status=401)


@app.route('/api/v1.0/foto', methods=['POST'])
@cross_origin(origin='*', headers=['Content-Type','Authorization'])
def foto():
    try:
        # Validate request data format
        content_type = request.headers.get('Content-Type')
        if ('application/x-www-form-urlencoded' not in content_type and
            'multipart/form-data' not in content_type ):
            return Response(status=415)

        usuario = request.form['usuario']
        apikey = request.form['apikey']

        user = User.query.filter_by(name=usuario).first()
        if user is None or user.apikey != apikey:
            # Si el usuario no existe o la apikey es invalida salgo
            return Response(status=401)

        f = request.files['foto']
        f.save(os.path.join(UPLOAD_FOLDER, f"{usuario}.png"))
        return redirect(url_for('blog', usuario=usuario))
    except:
        return Response(status=400)

@app.route('/api/v1.0/reset')
def reset():
    try:
        usuario = request.args.get('usuario')
        apikey = request.args.get('apikey')

        if usuario is None or apikey is None:
            return Response(status=401)

        user = User.query.filter_by(name=usuario).first()
        if user is None or user.apikey != apikey:
            # Si el usuario no existe o la apikey es invalida salgo
            return Response(status=401)

        db.session.remove()
        db.drop_all()
        db.create_all()
        return Response(status=200)

    except Exception as e:
        print(e)
        print(jsonify({'trace': traceback.format_exc()}))
        return Response(status=401)

# Este método se ejecutará solo una vez
# la primera vez que ingresemos a un endpoint
@app.before_first_request
def before_first_request_func():
    # Crear aquí todas las bases de datos
    db.create_all()
    print("Base de datos generada")


if __name__ == '__main__':
    print('Inove@Server start!')

    # Lanzar server
    app.run(host="127.0.0.1", port=5000)