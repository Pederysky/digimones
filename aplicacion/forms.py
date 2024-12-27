from flask_wtf import FlaskForm
from wtforms import Form, IntegerField,SelectField,SubmitField,StringField, DecimalField, TextAreaField, FileField
from wtforms.validators import InputRequired
from flask_wtf import FlaskForm
from wtforms import StringField, IntegerField, SelectField, SubmitField
from wtforms.validators import DataRequired, Optional, NumberRange, URL
from flask_wtf.file import FileField, FileAllowed
#Nuevo 7_4
from wtforms import StringField, SubmitField, DecimalField, IntegerField,\
    TextAreaField, SelectField, PasswordField, EmailField

class formArticulo(FlaskForm): 
	nombre=StringField("Nombre:",validators=[InputRequired("Tienes que introducir el dato")])
	precio=DecimalField("Precio:",default=0,validators=[InputRequired("Tienes que introducir el dato")])
	iva=IntegerField("IVA:",default=21,validators=[InputRequired("Tienes que introducir el dato")])
	descripcion= TextAreaField("Descripción:")
	photo = FileField('Selecciona imagen:')
	stock=IntegerField("Stock:",default=1,validators=[InputRequired("Tienes que introducir el dato")])
	CategoriaId=SelectField("Categoría:",coerce=int)
	submit = SubmitField('Enviar')


class FormCategoria(FlaskForm):
    nombre = StringField("Nombre:",
                        validators=[InputRequired("Tienes que introducir el dato")]
                        )
    submit = SubmitField('Enviar')
    

class FormTipo(FlaskForm):
    tipo = StringField("Tipo:",
                        validators=[InputRequired("Tienes que introducir el dato")]
                        )
    submit = SubmitField('Enviar')
    
    
class FormDigimones(FlaskForm): 
	nombre=StringField("Nombre:",validators=[InputRequired("Tienes que introducir el dato")])
	ataque=IntegerField("Ataque:",default=0,validators=[InputRequired("Tienes que introducir el dato")])
	defensa=IntegerField("Defensa:",default=0,validators=[InputRequired("Tienes que introducir el dato")])
	nivel= SelectField("Nivel:",choices=[('Inicial', 'Bebito'), ('Medio', 'Ya sabe algo'),('Experto','Se mucho Flask'),('Experto','Puto Amo')])
	imagen = FileField('Imagen', validators=[
        FileAllowed(['jpg', 'png', 'jpeg', 'gif'], 'Solo se permiten imágenes.')
    ])
	TipoId=SelectField("Tipo:",coerce=int)
	submit = SubmitField('Enviar')    

class FormSINO(FlaskForm):
    si = SubmitField('Si')
    no = SubmitField('No')
    

#Filtrar Digimones
class FormBuscarDigimon(FlaskForm):
    campo = SelectField("Campo a buscar:", choices=[('nombre', 'Nombre'), ('ataque', 'Ataque'), ('defensa', 'Defensa')], validators=[InputRequired("Selecciona un campo")])
    modo = SelectField("Modo de búsqueda:", choices=[('Empieza', 'Empieza'), ('Acaba', 'Acaba'), ('Contiene', 'Contiene'), ('Igual', 'Igual')], validators=[InputRequired("Selecciona un modo")])
    palabra = StringField("Término de búsqueda:", validators=[InputRequired("Introduce un término de búsqueda")])
    submit = SubmitField('Buscar')

#Añadir Digimon
class DigimonForm(FlaskForm):
    nombre = StringField('Nombre', validators=[DataRequired()])
    ataque = IntegerField('Ataque', validators=[DataRequired(), NumberRange(min=0, message="El número debe ser positivo")])
    defensa = IntegerField('Defensa', validators=[DataRequired(), NumberRange(min=0, message="El número debe ser positivo")])
    imagen = FileField('Imagen', validators=[
        FileAllowed(['jpg', 'png', 'jpeg', 'gif'], 'Solo imágenes permitidas.')
    ])
    nivel = IntegerField('Nivel', validators=[DataRequired(), NumberRange(min=0, message="El número debe ser positivo")])
    TipoId = SelectField('Tipo', validators=[DataRequired()], choices=[])
    submit = SubmitField('Agregar Digimon')



class FormTipoEdit(FlaskForm):
    tipo = SelectField('Nuevo Tipo', coerce=int)



#Nuevo 7_4
class FormUsuario(FlaskForm):
    username = StringField('Login', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    nombre = StringField('Nombre completo')
    email = EmailField('Email')
    submit = SubmitField('Aceptar')


class FormChangePassword(FlaskForm):
    password = PasswordField('Password', validators=[DataRequired()])
    submit = SubmitField('Aceptar')

class LoginForm(FlaskForm):
    username = StringField('Login', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    submit = SubmitField('Entrar')