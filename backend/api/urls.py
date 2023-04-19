from django.urls import path, include
from . import views

urlpatterns = [
	path('', views.home, name='home page'),
	path('gen-api-key', views.generateAPIKey, name='generate api key'),
	path('search', views.search, name='search'),
	path('results', views.results, name='results'),
	path('export-menu', views.export_menu, name='export menu'),
	path('view/<str:name>', views.product_view, name='view'),
	path('add/<str:name>', views.addProduct, name='add product'),
	path('delete/<str:name>', views.deleteProduct, name='delete product'),
	path('cart', views.loadCart, name='load cart'),
	path('compare', views.compareItems, name='compare items'),
	path('quantity/<str:name>', views.editQuantity, name='edit quantity'),

]
