from django import forms

class libro_mes_form(forms.Form):
	#fecha_ini = forms.DateField(widget = forms.TextInput(), label='Fecha Inicial')
	fecha_consulta = forms.DateField(widget = forms.TextInput)


class fecha_mes_form(forms.Form):
	#fecha_ini = forms.DateField(widget = forms.TextInput(), label='Fecha Inicial')
	fecha = forms.DateField(widget = forms.TextInput)


class reporte_busqueda_form(forms.Form):
	fecha_ini = forms.DateField()
	fecha_fin = forms.DateField()
	
	#fecha_ini = forms.DateField(widget = forms.TextInput(attrs={'id':'datepicker'}), label='Fecha Inicial')
	#fecha_fin = forms.DateField(widget = forms.TextInput(attrs={'id':'datepicker1'}), label='Fecha Final')
	#reporte1 = forms.BooleanField(widget = forms.CheckboxInput, required=False, initial=True)
	