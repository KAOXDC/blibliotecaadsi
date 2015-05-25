# Create your views here.
# Vistas de la aplicacion libros
from django.shortcuts import render_to_response
from django.template import RequestContext
from biblioteca.apps.libros.forms import *#add_prestamo_form, add_autor_form, delete_prestamo_form, edit_prestamo_form, edit_autor_form, add_editorial_form, add_categoria_form, add_bibliotecario_form, edit_bibliotecario_form, add_usuario_form, edit_usuario_form, add_ciudad_form, edit_ciudad_form, add_tipo_usuario_form, agregar_libro_form, agregar_biblioteca_form
from biblioteca.apps.libros.models import *#Prestamo, Autor, Editorial, Categoria, Bibliotecario, Usuario, Ciudad, Tipo_Usuario, Libro, Biblioteca
from django.http import HttpResponseRedirect

from django.contrib.auth.models import User
from datetime import date



def administrar_view (request):
	return render_to_response('libros/administrar.html', context_instance = RequestContext(request))

def add_prestamo_view(request,id_libro): #crear una reserva en estado RESERVADO
	info = "" 
	#if request.user_is_authenticated() and request.user_is_staff():#modificado el 10 de abril
	if request.method == "POST": #si es POST
		formulario = add_prestamo_form(request.POST)
		if formulario.is_valid():
			add = formulario.save(commit =False)
			x = Libro.objects.get(id=id_libro)# modificacion 20 marzo 2015
			add.libro = x

			'''  conectar bibliotecario con usuario'''
			
			'''obtetener el usuario que realizo la reserva'''
			try: # 15 de mayo 2015 +++
				
				y = Usuario.objects.get(tipo_usuario__nombre = "bibliotecario", user_id = request.user.id)
				add.bibliotecario = y 	
				print request.user 
			except:
				print "debe estar logueado"
			#estado_prestamo reservado, cancelado, efectuado
			try:
				if request.user_is_authenticated and request.user_is_staff:
					add.usuario = Usuario.objects.get(user__id = request.user.id)
					
			except:
				info = "nose pudo guardar" # +++
			if x.disponibilidad == True:
				add.estado_prestamo = "reservado"
				x.disponibilidad = False
			else:
				mensaje="el libro no esta disponible"
			x.save()
			add.save() # guarda la informacion
			info = "Guardado Satisfactoriamente"
			return HttpResponseRedirect ('/prestamos/')
	else:
		formulario = add_prestamo_form()
	ctx = {'form':formulario, 'informacion': info}
	return render_to_response('libros/add_prestamo.html', ctx, context_instance = RequestContext(request))


def prestar_view(request, id_prestar):  #modificado el 17 de abril Funcion prestar
	info = ""
	usu = ""
	pres = Prestamo.objects.get(pk = id_prestar)
	if usu:
		try:
			usu = Usuario.objects.get(tipo_usuario__nombre = "bibliotecario", user_id = request.user.id)
			pres.estado_prestamo = "efectuado"
			pres.bibliotecario = "bibliotecario"
			pres.save()
			info = "Guardo Satisfactoriamente"
		except:
			print "no se pudo efectuar el prestamo"
	#return HttpResponseRedirect ('/prestamos/')
	return HttpResponseRedirect ('/prestamo/%s'%(pres.id))
###

#	ctx = {'form':formulario, 'informacion':info}
#	return render_to_response('libros/edit_prestamo.html',ctx , context_instance = RequestContext(request))

def edit_prestamo_view(request, id_editprest):
	info = ""
	editprest = Prestamo.objects.get(pk = id_editprest)
	if request.method == "POST":
		formulario = add_prestamo_form(request.POST, instance=editprest)
		if formulario.is_valid():
			edit_prestamo = formulario.save(commit = False)
			
			edit_prestamo.save()
			info = "Guardo Satisfactoriamente"
			return HttpResponseRedirect ('/prestamos/')

	else:
		formulario = add_prestamo_form(instance = editprest)

	ctx = {'form':formulario, 'informacion':info}
	return render_to_response('libros/edit_prestamo.html',ctx , context_instance = RequestContext(request))

def eliminar_prestamo_view(request, id_prest):
	info = "el prestamo se elimino safisfactoriamente"
	prest = Prestamo.objects.get(pk = id_prest)
	
	try:
		prest.delete()
		return HttpResponseRedirect ('/prestamos/')

	except:
		info = "La prestamo no existe"
		return HttpResponseRedirect ('/prestamos/')



#autor
def add_autor_view(request):
	info = "" #inicializando
	if request.method == "POST": #si es POST
		formulario = add_autor_form(request.POST)
		if formulario.is_valid():
			add = formulario.save(commit =False)
			add.save() # guarda la informacion
			info = "Guardado Satisfactoriamente"
			return HttpResponseRedirect ('/autores/')
	else:
		formulario = add_autor_form()
	ctx = {'form':formulario, 'informacion': info}
	return render_to_response('libros/add_autor.html', ctx, context_instance = RequestContext(request))

def edit_autor_view(request, id_editautor):
	info = ""
	editautor = Autor.objects.get(pk = id_editautor)
	if request.method == "POST":
		formulario = add_autor_form(request.POST, instance=editautor)
		if formulario.is_valid():
			edit_autor = formulario.save(commit = False)
			
			edit_autor.save()
			info = "Guardo Satisfactoriamente"
			return HttpResponseRedirect ('/autores/')

	else:
		formulario = edit_autor_form(instance = editautor)

	ctx = {'form':formulario, 'informacion':info}
	return render_to_response('libros/edit_autor.html',ctx , context_instance = RequestContext(request))


def eliminar_autor_view(request, id_aut):
	info = "el autor...."
	aut = Autor.objects.get(pk = id_aut)
	
	try:
		aut.delete()
		return HttpResponseRedirect ('/autores/')

	except:
		info = "El autor no existe!!!!"
		return HttpResponseRedirect ('/autores/')

#editorial
def add_editorial_view(request):
	info = ""
	if request.method =="POST": #SI ES POST
		formulario = add_editorial_form(request.POST)
		if formulario.is_valid():
			add = formulario.save(commit = False)
			add.save()
			info = "Guardado Satisfactoriamente"
			return HttpResponseRedirect ('/editoriales/')
			
			
			informacion = "Se Guardo Satisfactoriamente"
	else:
		formulario = add_editorial_form()
	ctx = {'form':formulario,'info': info}
	return render_to_response('libros/add_editorial.html', ctx,context_instance = RequestContext(request))



def edit_editorial_view(request, id_editorial):
	info =""
	editorial = Editorial.objects.get(pk = id_editorial)

	if request.method == "POST":
		formulario = add_editorial_form(request.POST, instance = editorial)
		if formulario.is_valid():
			edit_editorial = formulario.save(commit = False)
			edit_editorial.save()
			info = " Guardado Satisfactoriamente"
			return HttpResponseRedirect ('/editoriales/')
	else:
		formulario = add_editorial_form(instance = editorial)
	ctx = {'form':formulario, 'informacion':info}
	return render_to_response('libros/edit_editorial.html', ctx,context_instance = RequestContext(request))

			
def eliminar_editorial_view(request, id_editorial):
	info = ""
	editorial = Editorial.objects.get (pk = id_editorial)

	try:
		editorial.delete()
		return HttpResponseRedirect('/editoriales/')

	except:
		info = "la Editorial Que desea Eliminar No Existe"
		return render_to_response ('/editoriales')

#categoria
def add_categoria_view(request):
	info = "inicializando"
	if request.method == "POST":
		formulario = add_categoria_form(request.POST, request.FILES)
		if formulario.is_valid():
			add = formulario.save (commit = False)
			add.save()
			info = "Guardado Satisfactoriamente"
			return HttpResponseRedirect ('/categorias')
	else:
		formulario = add_categoria_form()
	ctx = {'form':formulario, 'informacion':info}
	return render_to_response ('libros/agregar_categoria.html', ctx,context_instance =RequestContext(request))

def editar_categoria_view (request, id_prod):
	info = ""
	prod = Categoria.objects.get(pk = id_prod)
	if request.method =="POST":
		formulario = add_categoria_form(request.POST, instance= prod)
		if formulario.is_valid():
			edit_prod = formulario.save(commit = False) 
			edit_prod.save()
			info ="Guardado Satisfactoriamente"
			return HttpResponseRedirect ('/categorias')
	else:
		formulario = add_categoria_form(instance = prod)

	ctx = {'form': formulario, 'informacion':info}
	return render_to_response('libros/editar_categoria.html', ctx, context_instance= RequestContext(request))

def eliminar_categoria_view(request, id_prod):
	info = "la categoria se elimino safisfactoriamente"
	prod = Categoria.objects.get(pk = id_prod)
	
	try:
		prod.delete()
		return HttpResponseRedirect ('/categorias')

	except:
		info = "La categoria no existe"
		return HttpResponseRedirect ('/categorias')



#bibliotecario
def add_bibliotecario_view(request):
	info = "inicializando"
	if request.method == "POST":
		formulario = add_bibliotecario_form(request.POST)
		if formulario.is_valid():
			add = formulario.save(commit = False)

			add.save() # guarda la informacion
		# guarda las relaciones ManyToMany
			info = "Guardado Satisfactoriamente"
			return HttpResponseRedirect ('/bibliotecarios/')
	else:
		formulario = add_bibliotecario_form()
	ctx = {'form':formulario, 'informacion':info}
	return render_to_response('libros/add_bibliotecario.html', ctx,context_instance = RequestContext(request))

def edit_bibliotecario_view(request, id_biblio):
	info = ""
	biblio = Bibliotecario.objects.get(pk = id_biblio)
	if request.method == "POST":
		formulario = add_bibliotecario_form(request.POST, instance= biblio )
		if formulario.is_valid():
			edit_biblio = formulario.save(commit = False)
	
			edit_biblio.save()
			info = "Guardado Satisfactoriamente"
			return HttpResponseRedirect('/bibliotecarios/')
	else:
		formulario = add_bibliotecario_form(instance = biblio)
	ctx = {'form':formulario, 'informacion':info}
	return render_to_response('libros/edit_bibliotecario.html', ctx,context_instance = RequestContext(request))

def del_bibliotecario_view(request, id_biblio):
	info = "inicializando"
	biblio = Bibliotecario.objects.get(pk = id_biblio)
	try:
		biblio.delete()
		return HttpResponseRedirect('/bibliotecarios')
	except:
		info = "Bibliotecario no se puede eliminar"
		return HttpResponseRedirect('/bibliotecarios')

#usuario
def add_usuario_view(request):
	info = "inicializando"
	if request.method == "POST": #si es POST
		formulario = add_usuario_form(request.POST)
		if formulario.is_valid():
			add = formulario.save(commit =False)
			add.save() # guarda la informacion
			info = "Guardado Satisfactoriamente"
			return HttpResponseRedirect ('/usuarios/')
	else:
		formulario = add_usuario_form()
	ctx = {'form':formulario, 'informacion': info}
	return render_to_response('libros/add_usuario.html', ctx,context_instance = RequestContext(request))





def edit_usuario_view(request, id_usua):
	info = ""
	usua = Usuario.objects.get(pk = id_usua)
#	usn  = usua.user.username
#	ema  = usua.user.email
	if request.method == "POST":
		formulario = add_usuario_form(request.POST, request.FILES, instance=usua)
		formulario_user = edit_user_form(request.POST, instance = usua.user)
		if formulario.is_valid() and formulario_user.is_valid():
			edit_usua = formulario.save(commit = False)
			#e_user = 	
			#x = formulario_user.cleaned_data['password']
			edit_usua.save()
			usua.user.set_password(formulario_user.cleaned_data['clave'])
			#formulario_user.set_password("123123")
			formulario_user.save()
			info = "Guardado Satisfactoriamente"
			return HttpResponseRedirect('/usuarios/')
	else:
		formulario = add_usuario_form(instance = usua)
		formulario_user = edit_user_form(instance = usua.user)
	ctx = {'form':formulario, 'informacion':info, 'form_user': formulario_user}
	return render_to_response('libros/edit_usuario.html', ctx,context_instance = RequestContext(request))


def del_usuario_view(request,id_usua):
	info = "Se inicio proceso de eliminacion del Usuario" 
	usua = Usuario.objects.get(pk = id_usua)
	try:
		usua.delete()
		return HttpResponseRedirect ('/usuarios')
	except:
		info= "El Usuario que desea eliminar no existe"
		#return render_to_response('home/usuario.html')
		return HttpResponseRedirect ('/usuarios')

#tipo_usuario
def add_tipo_usuario_view(request):
	info = "inicializando"
	if request.method == "POST": #si es POST
		formulario = add_tipo_usuario_form(request.POST)
		if formulario.is_valid():
			add = formulario.save(commit =False)
			add.save() # guarda la informacion
			info = "Guardado Satisfactoriamente"
			return HttpResponseRedirect ('/tipos_usuarios/')
	else:
		formulario = add_tipo_usuario_form()
	ctx = {'form':formulario, 'informacion': info}
	return render_to_response('libros/add_tipo.html', ctx,context_instance = RequestContext(request))


def edit_tipo_usuario_view(request, id_tipo):
	info = ""
	tipo = Tipo_Usuario.objects.get(pk = id_tipo)
	if request.method == "POST":
		formulario = add_tipo_usuario_form(request.POST, request.FILES, instance=tipo)
		if formulario.is_valid():
			edit_tipo = formulario.save(commit = False)
			
			edit_tipo.save()
			info = "Guardo Satisfactoriamente"
			return HttpResponseRedirect ('/tipos_usuarios/')

	else:
		formulario = add_tipo_usuario_form(instance = tipo)

	ctx = {'form':formulario, 'informacion':info}
	return render_to_response('libros/edit_tipo.html',ctx , context_instance = RequestContext(request))

def eliminar_tipo_usuario_view(request, id_tipo):
	info = "El tipo de usuario se elimino satisfactoriamente"
	

	try:
		tipo = Tipo_Usuario.objects.get(pk = id_tipo)
		tipo.delete()
		return HttpResponseRedirect('/tipos_usuarios')
	except:
		info = "El tipo de usuario que desea eliminar no existe"
		return HttpResponseRedirect ('/tipos_usuarios')   

#ciudad
def add_ciudad_view(request):
	info = "inicializando"
	if request.method == "POST":
		formulario = add_ciudad_form(request.POST)
		if formulario.is_valid():
			add = formulario.save(commit = False)

			add.save() # guarda la informacion
		# guarda las relaciones ManyToMany
			info = "Guardado Satisfactoriamente"
			return HttpResponseRedirect ('/ciudades/')
	else:
		formulario = add_ciudad_form()
	ctx = {'form':formulario, 'informacion':info}
	return render_to_response('libros/add_ciudad.html', ctx,context_instance = RequestContext(request))



def edit_ciudad_view(request, id_ciu):
	info = ""
	ciu = Ciudad.objects.get(pk = id_ciu)
	if request.method == "POST":
		formulario = add_ciudad_form(request.POST, instance= ciu)
		if formulario.is_valid():
			edit_ciu = formulario.save(commit = False)
	
			edit_ciu.save()
			info = "Guardado Satisfactoriamente"
			return HttpResponseRedirect('/ciudades/')
	else:
		formulario = add_ciudad_form(instance = ciu)
	ctx = {'form':formlario, 'informacion':info}
	return render_to_response('libros/edit_ciudad.html', ctx,context_instance = RequestContext(request))

def del_ciudad_view(request, id_ciu):
	info = "inicializando"
	ciu = Ciudad.objects.get(pk = id_ciu)
	try:
		ciu.delete()
		return HttpResponseRedirect('/ciudades')
	except:
		info = "Ciudad no se puede eliminar"
		return HttpResponseRedirect('/ciudades')	


#libro
def agregar_libro_view (request):
	info = "inicializando"
	if request.method == "POST":
		formulario = agregar_libro_form(request.POST, request.FILES)
		if formulario.is_valid():
			add = formulario.save(commit = False)
			add.save()
			formulario.save_m2m()
			info = "Guardado satisfactoriamente"
			return HttpResponseRedirect ('/libros')
	else:
		formulario = agregar_libro_form()
	ctx = {'form':formulario, 'informacion':info}
	return render_to_response('libros/agregar_libro.html', ctx,context_instance = RequestContext(request))

 
def editar_libro_view (request, id_prod):
	info = ""
	prod = Libro.objects.get(pk = id_prod)
	if request.method == "POST":
		formulario = agregar_libro_form(request.POST, instance= prod) #FILES para agregar imagenes
		if formulario.is_valid():
			edit_prod = formulario.save(commit = False)
			formulario.save_m2m()
			edit_prod.save()
			info = "Guardado satisfactoriamente"
			return HttpResponseRedirect ('/libros')
	else:
		formulario = agregar_libro_form(instance = prod)

	ctx = {'form':formulario, 'informacion':info}
	return render_to_response('libros/editar_libro.html', ctx,context_instance = RequestContext(request))


def del_view (request, id_prod): 
	info = "Se inicio el proceso de eliminacion"
	prod = Libro.objects.get(pk = id_prod)

	try:
		prod.delete()
		return HttpResponseRedirect ('/libros')#cuando no se trabaja con paginator se agrega sin numero 
	except: 
		info = "EL libro que desea eliminar no existe"
		return HttpResponseRedirect ('/libros')


#biblioteca

def agregar_biblioteca_view(request):
	info ="inicializando"
	if request.method == "POST":
		formulario = agregar_biblioteca_form(request.POST)
		if formulario.is_valid():
			add = formulario.save(commit = False)
			add.save()#guarda la informacion
			info = "Guardo Satisfactoriamente"
			return HttpResponseRedirect ('/bibliotecas/')
	else:
		formulario =agregar_biblioteca_form()
	ctx = {'form':formulario,'informacion':info}
	return render_to_response('libros/agregar_biblioteca.html',ctx,context_instance = RequestContext(request))


def editar_biblioteca_view(request,id_biblioteca):
	info =""
	biblioteca = Biblioteca.objects.get(pk =id_biblioteca)

	if request.method == "POST":
		formulario = agregar_biblioteca_form(request.POST, instance= biblioteca)
		if formulario.is_valid():
			edit_biblioteca= formulario.save(commit = False)
			edit_biblioteca.save()
			info = "Guardo Satisfactoriamente"
			return HttpResponseRedirect ('/bibliotecas/')
	else:
		formulario = agregar_biblioteca_form(instance = biblioteca)

	ctx = {'form':formulario,'informacion':info}
	return render_to_response('libros/editar_biblioteca.html',ctx,context_instance = RequestContext(request))


def eliminar_biblioteca_view(request, id_biblioteca):
	info = "la biblioteca se elimino Satisfactoriamente"
	biblioteca = Biblioteca.objects.get(pk = id_biblioteca)

	try:
		biblioteca.delete()
		return HttpResponseRedirect ('/bibliotecas')

	except:
		info = "la biblioteca no existe"
		return render_to_response ('/bibliotecas')

#buscar

def add_buscar_view(request):
	libros = []
	categorias = []
	autores = []
	editoriales = []
	codigo =[]
	busqueda = ""
	mensaje =""
	info = "inicializando"
	if request.method == "POST": #si es POST
		formulario = add_buscar_form(request.POST)
		busqueda = request.POST['busqueda']	
		if formulario.is_valid():
		#agregar	
			busqueda = formulario.cleaned_data['busqueda']
			add = formulario.save(commit =False)
			#add.save() # guarda la informacion
			info = "Guardado Satisfactoriamente"
			#buscar
			try:
				editoriales = Libro.objects.filter(editorial__nombre = busqueda, disponibilidad = True)
				libros= Libro.objects.filter(nombre_libro= busqueda)
				autores = Libro.objects.filter(autor__nombre = busqueda, disponibilidad = True)

				cat = Categoria.objects.get(nombre=busqueda)
				categorias = Libro.objects.filter(categoria = cat)

				
				

				#codigo = Libro.objects.get(codigo= int(busqueda)) 
				
			except:
				mensaje = ""
				#libro = Libro.objects.all(request.POST)
			if libros or categorias or autores or editoriales:
				add.resultados=True
			else:
				add.resultados=False
			add.save()
			print "-------------------------\n"
			print editoriales
	else:
		formulario = add_buscar_form()
	ctx = {'form':formulario, 'informacion': info, 'mensaje':mensaje, 'libro':libros, 'categoria':categorias, 'autor':autores, 'editorial':editoriales, 'busqueda':busqueda}
	return render_to_response('libros/add_buscar.html', ctx,context_instance = RequestContext(request))

#consultar usuario (maria y cesar se aman)
def consultar_usuario_id_view(request):
	mensaje = ""
	usua =""
	if request.user.is_authenticated():
		if request.method == "POST":
			formulario	 = consultar_usuario_id_form(request.POST) #creamos un objeto de Loguin form
			if formulario.is_valid(): #si la informacion enviada es correcta
				tipo_id=formulario.cleaned_data['tipo_id']
				ide= formulario.cleaned_data['identificacion'] #guarda informacion ingresada del formulario
				try:
					usua=Usuario.objects.get(tipo_id=tipo_id,identificacion=ide)
					mensaje = "Se encontro el Usuario con el Numero de Identificacion " + ide + " sus Datos son:"

					#return HttpResponseRedirect('/usuario/%s'%usua.id)		
				except:
					mensaje = "Usuario no encontrado" #verificampos si el usuario ya esta autenticado o logueado}
			else:
				mensaje = "El campo no debe estar vacio, por favor ingrese un valor"
						
	 #si esta logueando lo redirigimos a la pagina principal
	else: #si no esta authenticado
		return HttpResponseRedirect('/')
	formulario = consultar_usuario_id_form() #creamos un formulario nuevo en limpio
	ctx = {'form':formulario, 'mensaje':mensaje, 'usuario':usua} # variable de contexto para pasar info a login.html
	return render_to_response('home/consultar.html', ctx,context_instance = RequestContext(request))

#register view

def register_view(request):
		now = date.today()
		if request.method == "POST":
			form_a = RegisterForm(request.POST)
			form_b = add_usuario_form(request.POST, prefix = "b")
			if form_b.is_valid() and form_a.is_valid():
				usuario 		= form_a.cleaned_data['username']
				email 			= form_a.cleaned_data['email']
				password_one	= form_a.cleaned_data['password_one']
				password_two 	= form_a.cleaned_data['password_two']

				u = User.objects.create_user(username = usuario,email = email, password = password_one)
				u.save() #guarda el objeto
				
				b = form_b.save(commit=False)


				'''b.add_usuario_form = a
				'''
				b.user= u 
				
				b.save()
				return render_to_response('home/confirmacion.html',context_instance = RequestContext(request))
			else:
				info = "fallo"	
		else:
			form_a = RegisterForm()
			form_b = add_usuario_form(prefix = "b")
		ctx = {'form_a':form_a, 'form_b':form_b, 'now':now}	
		return render_to_response ('home/register.html',ctx, context_instance= RequestContext(request))	
