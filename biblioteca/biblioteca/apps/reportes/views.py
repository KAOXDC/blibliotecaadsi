# Create your views here.
from django.shortcuts import render_to_response
from django.template import RequestContext
from django.forms import extras
from django.core.paginator import Paginator, EmptyPage, InvalidPage
from django.views.generic import TemplateView
from django.shortcuts import render
from django.contrib.auth import authenticate
from django.http import HttpResponseRedirect
from biblioteca.apps.reportes.forms import  *
from biblioteca.apps.libros.forms import *
from biblioteca.apps.libros.models import *
from datetime import  date, timedelta

def reportes_view(request):
	if request.user.is_authenticated():
		return render_to_response('home/reportes.html',context_instance = RequestContext(request)) 
	else:
		return HttpResponseRedirect('/')


def reporte_libros_mes_view(request):
	if request.user.is_authenticated():
		info_enviado = True
		fecha_libro = ""
		#hoy = date.today()
		#mes = hoy.month
		mes = 0
		anio = 0
		prest_libro = []

		if request.method == "POST":
			reportes = libro_mes_form(request.POST)
			if reportes.is_valid():
				info_enviado = True
				fecha_libro = reportes.cleaned_data['fecha_consulta']
				mes = fecha_libro.month
				anio = fecha_libro.year
				prest_libro = Prestamo.objects.filter(fecha_prestamo__month = mes, fecha_prestamo__year = anio)
		else:                                                                  
			reportes = libro_mes_form()
		ctx = {'reporte_libro':reportes, 'prest_libro':prest_libro, 'info_enviado':info_enviado, 'fecha_libro':fecha_libro }
		return render_to_response('reportes/reporte_libro_mes.html',ctx, context_instance = RequestContext(request)) 
	else:
		return HttpResponseRedirect('/')


def reporte_usuarios_mes_view(request):
	if request.user.is_authenticated():
		info_enviado = True
		fecha_usuarios = ""
		#hoy = date.today()
		#mes = hoy.month
		mes = 0
		anio = 0
		usuarios = []
		mensaje = ""
		error_fecha = ""
		error_vacio = ""
		
		if request.method == "POST":
			reportes = fecha_mes_form(request.POST)
			if reportes.is_valid():
				info_enviado = True
				fecha_usuarios= reportes.cleaned_data['fecha']
				if fecha_usuarios <= date.today():
					mes = fecha_usuarios.month
					anio = fecha_usuarios.year
					usuarios = Prestamo.objects.filter(fecha_prestamo__month =mes,fecha_prestamo__year = anio)
					mensaje = "Exito!"
				else:
					error_fecha = "Error! La Fecha Igresada no Puede Ser Mayor a la Fecha Actual"
			else:
				error_vacio = "el campo no debe estar vacio"


		else:                                                                  
			reportes = fecha_mes_form()
		ctx = {'reporte_usuarios':reportes,'mensaje':mensaje,'error_vacio':error_vacio,'error_fecha':error_fecha, 'usuarios':usuarios, 'info_enviado':info_enviado, 'fecha_usuarios':fecha_usuarios }
		return render_to_response('reportes/reporte_usuarios_mes.html',ctx, context_instance = RequestContext(request)) 
	else:
		return HttpResponseRedirect('/')

def reporte_busqueda_view(request):
	info_enviado = True
	fecha_inicio = ""
	fecha_final = ""
	busqueda = []
	#formulario = reporte_busqueda_form()
	if request.method == "POST": #Envio de informacion por POST
		reportes = reporte_busqueda_form(request.POST)
		print "---------------"
		if reportes.is_valid():
			info_enviado = True
			fecha_inicio = reportes.cleaned_data['fecha_ini']
			fecha_final = reportes.cleaned_data['fecha_fin']
			busqueda = Busqueda.objects.filter(fecha__range=(fecha_inicio, fecha_final))
			print "---------------", busqueda
			#S= busqueda.count()
	else: #GET
		reportes = reporte_busqueda_form()
	ctx = {'form':reportes,'busqueda':busqueda, 'reporte1':reportes,'info_enviado':info_enviado, 'fecha_ini':fecha_inicio, 'fecha_fin':fecha_final}		
	return render_to_response('reportes/reportes_busquedas.html',ctx, context_instance = RequestContext(request))
	