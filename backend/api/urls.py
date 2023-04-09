from django.urls import path, include
from . import views

urlpatterns = [
	#path('find-item', views.findItem, name='find items'),
	path('gen-api-key', views.generateAPIKey, name='generate api key'),
	path('search', views.search, name='search'),
	path('results', views.results, name='results'),
	path('view/<str:name>', views.product_view, name='view'),

]
