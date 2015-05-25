from django import forms
from biblioteca.apps.libros.models import *#Prestamo, Autor, Editorial, Categoria, Bibliotecario, Usuario, Ciudad, Tipo_Usuario, Libro, Biblioteca
from django.contrib.auth.models import User

from django.forms.extras import SelectDateWidget
from django.contrib.admin import widgets

tipo_id= (
	('cedula', 'Cedula'),
	('t.i', 'T.I'),
	('pasaporte', 'Pasaporte'),
	('libreta militar', 'Libreta Militar'),
)

#maria y cesar se aman ++++++
class consultar_usuario_id_form(forms.Form):
	identificacion= forms.CharField(widget = forms.TextInput())
	tipo_id = forms.ChoiceField(choices = tipo_id)

class edit_user_form(forms.ModelForm):
	clave = forms.CharField(widget=forms.PasswordInput(render_value=False), max_length= 140)
	class Meta:
		model   = User
		fields = {"username", "email", } 



#maria y cesar++++++++++++

class add_prestamo_form(forms.ModelForm):
	fecha_devolucion = forms.DateField(widget = forms.TextInput(attrs={'id':'datepicker'}), label='fecha_devolucion')
	class Meta:
		
		model 	= Prestamo
		exclude = {'libro', 'fecha_prestamo',  'bibliotecario','estado_prestamo',}#, 'estado_prestamo' } # <- modificacion el 13 de abril 
	
		#exclude = {'fecha_prestamo'}

class edit_prestamo_form(forms.ModelForm):
	class Meta:
		model 	= Prestamo

class delete_prestamo_form(forms.ModelForm):
	class Meta:
		model 	= Prestamo

#autor
class add_autor_form(forms.ModelForm):
	class Meta:
		model 	= Autor

class edit_autor_form(forms.ModelForm):
	class Meta:
		model 	= Autor

class delete_autor_form(forms.ModelForm):
	class Meta:
		model 	= Autor

# editorial
class add_editorial_form(forms.ModelForm):
	class Meta:
		model = Editorial

		exclude = {'status'}

#categoria
class add_categoria_form(forms.ModelForm):
	class Meta:
		model= Categoria

#bibliotecario
class add_bibliotecario_form(forms.ModelForm):
	class Meta:
		model   = Bibliotecario
		#se excluye el status por que en el modelo lo ponemos default=True

class edit_bibliotecario_form(forms.ModelForm):
	class Meta:
		model   = Bibliotecario 



class add_usuario_form(forms.ModelForm):
	fecha_nac = forms.DateField(widget = forms.TextInput(attrs={'id':'datepicker'}), label='Fecha de nacimiento')
	class Meta:
		model   = Usuario 
		exclude = {"user", }



#tipo_usuario
class add_tipo_usuario_form(forms.ModelForm):
	class Meta:
		model 	= Tipo_Usuario
		#se excluye el status por que en el modelo lo ponemos default=True

#ciudad
class add_ciudad_form(forms.ModelForm):
	class Meta:
		model   = Ciudad 

class edit_ciudad_form(forms.ModelForm):
	class Meta:
		model   = Ciudad 


#libro
class agregar_libro_form (forms.ModelForm): 
	class Meta:
		model = Libro
		#exclude = {"fecha_adquisicion" , "fecha_publicacion"}

#biblioteca
class agregar_biblioteca_form(forms.ModelForm):
	class Meta:
		model = Biblioteca

class add_buscar_form(forms.ModelForm):
	class Meta:
		model 	= Busqueda
		exclude = {'resultados'}


#proyecto maria--------
class RegisterForm(forms.Form):
	username 	= forms.CharField(label = "Nombre de Usuario", widget = forms.TextInput())
	email 		= forms.EmailField(label = "Correo Electronico", widget = forms.TextInput())
	password_one = forms.CharField(label = "Password", widget = forms.PasswordInput(render_value = False))
	password_two = forms.CharField(label = "Confirmar Password", widget = forms.PasswordInput(render_value = False))

	def clean_username(self):
		username = self.cleaned_data['username']
		try:
			u = User.objects.get(username = username)
		except User.DoesNotExist:
			return username
		raise forms.ValidationError('Nombre de Usuario ya Existe')

	def clean_email(self):
		email = self.cleaned_data['email']
		try:
			u = User.objects.get(email = email)
		except User.DoesNotExist:
			return email
		raise forms.ValidationError('Email ya registrado')

	def clean_password_two(self):
		password_one = self.cleaned_data['password_one']
		password_two = self.cleaned_data['password_two']

		if password_one == password_two:
			pass
		else:
			raise forms.ValidationError('Password no coinciden')
#proyecto maria--------