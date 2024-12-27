import os
from flask import Flask, render_template, redirect, url_for,abort, request, flash
from flask_bootstrap import Bootstrap
from flask_sqlalchemy import SQLAlchemy
from aplicacion import config
from werkzeug.utils import secure_filename
from aplicacion.forms import formArticulo, FormCategoria,FormSINO, FormTipo,FormDigimones, FormTipoEdit
from aplicacion.forms import FormBuscarDigimon, DigimonForm
#Nuevo 7_4
from flask_login import LoginManager, login_user, logout_user, login_required, current_user
from aplicacion.forms import LoginForm,FormUsuario, FormChangePassword


app = Flask(__name__)
app.config.from_object(config)
Bootstrap(app)
db = SQLAlchemy(app)
#Importamos los modelos una vez existe una instancia de app y otra instancia de db,
# En otras palabras si no hay base de datos, no puedo utilizar los modelos
# no base de datos (objeto) => No puedo acceder a las tablas
from aplicacion.models import *

#Nuevo 7_4
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = "login"


UPLOAD_FOLDER = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'static/uploads')
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['MAX_CONTENT_LENGTH'] = 2 * 1024 * 1024  # 2 MB

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/')
def bienvenido():
    return render_template ("bienvenido.html")

@app.route('/inicializar_datos')
def inicializar_datos():
    from aplicacion.inicializacion_datos import add_data_tables, drop_tables
    drop_tables()
    add_data_tables()
    return "Datos Inicializados"

@app.route('/tipos')
def tipos():
    tipos = Tipos.query.all()
    return render_template("tipos.html", tipos=tipos)

@app.route('/digimones')
@app.route('/tipo/<id>')
@login_required
def inicio(id='0'):
    tipo=Tipos.query.get(id)
    if id=='0':
        digimones=Digimones.query.all()
    else:
        digimones=Digimones.query.filter_by(TipoId=id)
    tipos=Tipos.query.all()
    return render_template("inicio.html",digimones=digimones,tipos=tipos,tipo=tipo)


@app.route('/tipos/new', methods=["get", "post"])
@login_required
def tipos_new():
    if not current_user.is_admin():
        abort(403)
    form = FormTipo()  
    if form.validate_on_submit():
        nuevo_tipo = Tipos(tipo=form.tipo.data)
        db.session.add(nuevo_tipo)
        db.session.commit()
        flash("Tipo agregado exitosamente", 'success')
        return redirect(url_for('tipos'))

    return render_template("tipos_new.html", form=form)

    
@app.route('/tipo/<id>/edit', methods=["get", "post"])
@login_required
def tipo_edit(id):
    if not current_user.is_admin():
        abort(403)
    tipo_actual = Tipos.query.get(id)
    form = FormTipo(obj=tipo_actual)
    if form.validate_on_submit():
        form.populate_obj(tipo_actual)
        db.session.commit()
        flash(f"El tipo ha sido modificado a '{tipo_actual.tipo}' exitosamente.")
        return redirect(url_for('tipos'))

    return render_template("tipo_edit.html", form=form, tipo=tipo_actual)


@app.route('/tipo/<id>/delete', methods=["get", "post"])
def tipo_delete(id):
    if not current_user.is_admin():
        abort(403)
    tipo = Tipos.query.get(id)
    
    if tipo is None:
        flash("El tipo no existe.")  
        return redirect(url_for('tipos'))
    
    form = FormSINO()
    
    if form.validate_on_submit():
        if form.si.data:
            db.session.delete(tipo)
            db.session.commit()
            flash(f"El tipo '{tipo.tipo}' ha sido eliminado correctamente.")
        else:
            flash("La eliminación del tipo ha sido cancelada.")
        
        return redirect(url_for('tipos'))
    
    return render_template("tipo_delete.html", tipo=tipo, form=form)


@app.route('/tipos/search', methods=['get', 'post'])
def tipos_search():
    palabra = request.args.get("palabra", "")
    tipos = []
    
    if palabra:
        tipos = Tipos.query.filter(Tipos.tipo.like(f"%{palabra}%")).all()
        if not tipos:
            flash(f"No se encontraron tipos que coincidan con '{palabra}'.")
    else:
        tipos = Tipos.query.all()
    
    return render_template("tipos.html", tipos=tipos, palabra=palabra)

#Añadir digimones  
@app.route('/digimones_new', methods=['get', 'post'])
def digimones_new():
    if not current_user.is_admin():
        abort(403)
    form = DigimonForm()
    form.TipoId.choices = [(tipo.id, tipo.tipo) for tipo in Tipos.query.all()]

    if form.validate_on_submit():
        if not os.path.exists(app.config['UPLOAD_FOLDER']):
            os.makedirs(app.config['UPLOAD_FOLDER'])

        if form.imagen.data and allowed_file(form.imagen.data.filename):
            filename = secure_filename(form.imagen.data.filename)
            filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            form.imagen.data.save(filepath)
        else:
            filename = None

        nuevo_digimon = Digimones(
            nombre=form.nombre.data,
            ataque=form.ataque.data,
            defensa=form.defensa.data,
            imagen=filename,
            nivel=form.nivel.data,
            TipoId=form.TipoId.data
        )
        db.session.add(nuevo_digimon)
        db.session.commit()
        flash('Digimon agregado exitosamente')
        return redirect(url_for('inicio'))

    return render_template('digimones_new.html', form=form)





#Modificar digimones
@app.route('/digimon/<id>/edit', methods=["get", "post"])
def digimon_edit(id):
    if not current_user.is_admin():
        abort(403)
    digimon = Digimones.query.get_or_404(id)

    form = DigimonForm(obj=digimon)
    form.TipoId.choices = [(tipo.id, tipo.tipo) for tipo in Tipos.query.all()]

    if form.validate_on_submit():
        if not os.path.exists(app.config['UPLOAD_FOLDER']):
            os.makedirs(app.config['UPLOAD_FOLDER'])

        if form.imagen.data and allowed_file(form.imagen.data.filename):
            filename = secure_filename(form.imagen.data.filename)
            filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            form.imagen.data.save(filepath)
            digimon.imagen = filename 
        else:
            filename = digimon.imagen 

        digimon.nombre = form.nombre.data
        digimon.ataque = form.ataque.data
        digimon.defensa = form.defensa.data
        digimon.nivel = form.nivel.data
        digimon.TipoId = form.TipoId.data
        db.session.commit()

        flash('Digimon actualizado exitosamente')
        return redirect(url_for('inicio')) 

    return render_template("digimones_edit.html", form=form, digimon=digimon)

# Borrar digimones
@app.route('/digimon/<id>/delete', methods=["get", "post"])
def digimon_delete(id):
    if not current_user.is_admin():
        abort(403)
    digimon = Digimones.query.get(id)
    if digimon:
        db.session.delete(digimon)
        db.session.commit()
        mensaje = f"El Digimon {digimon.nombre} ha sido eliminado correctamente."
    else:
        mensaje = "El Digimon no existe."

    return redirect(url_for('digimones_search', mensaje=mensaje))


def bienvenido():
    return render_template ("bienvenido.html")

@app.errorhandler(404)
def page_not_found(error):
    return render_template("error.html", error="Página no encontrada..."), 404



#Filtrar Digimones
@app.route('/digimones/search', methods=["get", "post"])
def digimones_search():
    form = FormBuscarDigimon()
    mensaje = request.args.get('mensaje')
    if form.validate_on_submit()    :
        campo = form.campo.data
        modo = form.modo.data
        palabra = form.palabra.data

        if modo == "Empieza":
            digimones = Digimones.query.filter(getattr(Digimones, campo).like(f"{palabra}%")).all()
        elif modo == "Acaba":
            digimones = Digimones.query.filter(getattr(Digimones, campo).like(f"%{palabra}")).all()
        elif modo == "Contiene":
            digimones = Digimones.query.filter(getattr(Digimones, campo).like(f"%{palabra}%")).all()
        elif modo == "Igual":
            digimones = Digimones.query.filter_by(**{campo: palabra}).all()
        else:
            digimones = Digimones.query.all()
    else:
        digimones = Digimones.query.all()

    return render_template("digimones_search.html", form=form, digimones=digimones, mensaje=mensaje)

#Nuevo 7_4
@app.errorhandler(403)
def permission_denied(error):
    return render_template("error_permisos.html", error="No tienes permisos para esto, prueba a contactar con el administrador"), 403

@app.route('/login', methods=['get', 'post'])
def login():
    from aplicacion.models import Usuarios
    # Control de permisos
    if current_user.is_authenticated:
        return redirect(url_for("inicio"))
    form = LoginForm()
    if form.validate_on_submit():
        user = Usuarios.query.filter_by(username=form.username.data).first()
        if user is not None and user.verify_password(form.password.data):
            login_user(user)
            next = request.args.get('next')
            return redirect(next or url_for('inicio'))
        form.username.errors.append("Usuario o contraseña incorrectas.")
    return render_template('login.html', form=form)


@app.route("/logout")
def logout():
    logout_user()
    return redirect(url_for('bienvenido'))


@app.route("/registro", methods=["get", "post"])
def registro():
    from aplicacion.models import Usuarios
    # Control de permisos
    if current_user.is_authenticated:
        return redirect(url_for("inicio"))
    form = FormUsuario()
    if form.validate_on_submit():
        existe_usuario = Usuarios.query.\
            filter_by(username=form.username.data).first()
        if existe_usuario is None:
            user = Usuarios()
            form.populate_obj(user)
            user.admin = False
            db.session.add(user)
            db.session.commit()
            return redirect(url_for("inicio"))
        form.username.errors.append("Nombre de usuario ya existe.")
    return render_template("usuarios_new.html", form=form)


@app.route('/perfil/<username>', methods=["get", "post"])
@login_required
def perfil(username):
    from aplicacion.models import Usuarios
    user = Usuarios.query.filter_by(username=username).first()
    if user is None or user.id!=current_user.id:
        abort(403)
    form = FormUsuario(request.form, obj=user)
    del form.password
    if form.validate_on_submit():
        form.populate_obj(user)
        db.session.commit()
        return redirect(url_for("inicio"))
    return render_template("usuarios_new.html", form=form, perfil=True)


@app.route('/changepassword/<username>', methods=["get", "post"])
@login_required
def changepassword(username):
    from aplicacion.models import Usuarios
    user = Usuarios.query.filter_by(username=username).first()
    if user is None or user.id!=current_user.id:
        abort(403)
    form = FormChangePassword()
    if form.validate_on_submit():
        form.populate_obj(user)
        db.session.commit()
        return redirect(url_for("inicio"))
    return render_template("changepassword.html", form=form)


@login_manager.user_loader
def load_user(user_id):
    from aplicacion.models import Usuarios
    return Usuarios.query.get(int(user_id))