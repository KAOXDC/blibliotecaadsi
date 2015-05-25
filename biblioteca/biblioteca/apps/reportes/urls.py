from django.conf.urls.defaults import patterns,url

urlpatterns = patterns('biblioteca.apps.reportes.views',
	url(r'^reportes/$', 'reportes_view', name = 'vista_reportes'),

#	url(r'^historia/(?P<id_his>.*)/$','singleHistoria_view',name='vista_single_historia'),

	url(r'^reportes/usuarios_por_mes/$', 'reporte_usuarios_mes_view', name = 'vista_reporte_usuarios_mes'),

	url(r'^reportes/libro_por_mes/$', 'reporte_libros_mes_view', name = 'vista_reporte_libros_mes'),
	
	url(r'^reporte_busqueda/$','reporte_busqueda_view', name = 'vista_reporte_busqueda'),

)
