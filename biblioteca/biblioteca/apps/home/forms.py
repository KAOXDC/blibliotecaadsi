from django import forms

class libronuevo_form(forms.Form):
	fecha_inicio	= forms.DateField(widget = forms.DateInput())

class Login_form(forms.Form):
	usuario 	= forms.CharField(widget = forms.TextInput())
	clave		= forms.CharField(widget = forms.PasswordInput(render_value = False))