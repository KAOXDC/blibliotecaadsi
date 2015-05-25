from django.db import models
from django.contrib.auth.models import User
#create here your models

tipo_id = (
	('cedula', 'cedula'),
	('ti', 'ti'),
	('pasaporte', 'pasaporte'),
	('libreta militar', 'libreta militar'),
)


class Tipo_Usuario (models.Model):
	nombre = models.CharField(max_length = 100)
	def __unicode__ (self):
		return self.nombre


genero= (
	('femenino', 'Femenino'),
	('masculino', 'Masculino'),
)


#estado prestamo 
estado_prestamo = (
	('reservado', 'Reservado'),
('cancelado', 'Cancelado'),
('efectuado', 'Efectuado'), 
	)

estado = (
	('bueno', 'Bueno'),

('regular','Regular'),
('malo', 'Malo'),
)




#Clase "Autor" Poto, George
class Autor (models.Model):
	nombre = models.CharField(max_length= 50)
	def __unicode__ (self):
		return self.nombre

#Clase "Tipo_Usuario" Yaki ft Jennifer

#Clase "Editorial" Las Primas
class Editorial (models.Model):
	nombre = models.CharField(max_length=200)

	def __unicode__ (self):
		return self.nombre

#Clase "Evelin ft Carolina"
class Categoria (models.Model):
	nombre = models.CharField(max_length = 200)

	def __unicode__(self):
		return self.nombre

# cuando una clase depende de otra esta se coloca al final, 
# como en este caso; la clase libro depende de la clase categoria 
#Clase "libro" Verito ft Sofi
class Libro (models.Model): 
	nombre_libro		= models.CharField(max_length = 200)
	autor				= models.ForeignKey(Autor)
	categoria			= models.ManyToManyField(Categoria, null = True, blank = True)
	editorial			= models.ForeignKey(Editorial)
	paginas				= models.IntegerField()
	version				= models.CharField(max_length = 10)
	tomo				= models.IntegerField()
	codigo				= models.IntegerField()
	estado				= models.CharField(max_length = 200, choices = estado)
	disponibilidad  	= models.BooleanField()
	fecha_adquisicion	= models.DateField()
	fecha_publicacion	= models.DateField()

	def __unicode__(self):
		return self.nombre_libro

#Clase "Biblioteca" Las Primas"
class Biblioteca (models.Model):
	nombre  	=models.CharField(max_length=200)
	direccion 	=models.CharField(max_length=200)
	telefono	=models.CharField(max_length=200)
	correo 		=models.CharField(max_length=200)
	reglamento  =models.CharField(max_length=200)

	def __unicode__ (self):
		return self.nombre


#Clase "Ciudad" Stefy ft Gomez
class Ciudad (models.Model):
	nombre = models.CharField(max_length = 200)
	
	def __unicode__ (self):
		return self.nombre



#Clase "Usuario" Mary ft Cesar
class Usuario (models.Model):

	def url (self,filename):
		ruta = "MultimediaData/Users/%s/%s"%(self.user.username, filename)
		return ruta

	nombre         			 = models.CharField(max_length = 100)
	apellido       			 = models.CharField(max_length = 100)
	tipo_id					 = models.CharField(max_length = 100, choices = tipo_id)
	identificacion     	   	 = models.CharField(max_length = 100)
	fecha_nac       	     = models.DateField()
	telefono        	   	 = models.CharField(max_length = 100)		
	direccion        	   	 = models.CharField(max_length = 100)
	genero					 = models.CharField(max_length = 200, choices = genero)
	ciudad                   = models.ForeignKey(Ciudad)
	tipo_usuario             = models.ForeignKey(Tipo_Usuario)
	user 					 = models.OneToOneField(User)
	photo 					 = models.ImageField(upload_to = url, null = True, blank = True)

	def __unicode__ (self):
		return self.nombre 

#Clase "Bibliotecario" Stefy ft Gomez 
class Bibliotecario (models.Model):
	nombre 			= models.CharField(max_length = 200)
	apellidos		= models.CharField(max_length = 200)
	telefono		= models.CharField(max_length = 200)
	direcccion		= models.CharField(max_length = 200)
	correo			= models.CharField(max_length = 200)
	genero			= models.CharField(max_length = 200, choices = genero)
	#usuario 		= models.()

	def __unicode__ (self):
		return self.nombre


#clase "Prestamo" Poto, George
class Prestamo (models.Model):
	fecha_prestamo 	=  models.DateField(auto_now =True) # 
	fecha_devolucion=  models.DateField() 
	libro 			=  models.ForeignKey(Libro)#
	bibliotecario   =  models.CharField(max_length=100 , null = True, blank = True) 
	usuario 		=  models.ForeignKey(Usuario)# como capturar el usuario logueado en django
	estado_prestamo =  models.CharField(max_length = 200, choices = estado_prestamo)#
	
	def __unicode__ (self):
		return self.libro.nombre_libro 

class Busqueda (models.Model):
	busqueda = models.CharField(max_length = 100)
	fecha 	 = models.DateTimeField(auto_now=True)
	resultados = models.BooleanField(default=True)

	def __unicode__ (self):
		return self.busqueda