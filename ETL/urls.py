from django.contrib import admin
from django.urls import path
from . import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.dashboard, name='dashboard'),
    path('achats/', views.show_achat_table, name='achat_table'),
    path('articles/', views.show_articles_table, name='articles_table'),
    path('ventes/', views.show_ventes_table, name='ventes_table'),
    path('bilan/', views.dashboard, name='dashboard'),
    path('analytic/', views.analytic, name='analytic'),
    path('upload/', views.upload_file, name='upload'),

    path('export/clients/', views.export_clients_to_excel, name='export_clients'),
    path('export/products/', views.export_products_to_excel, name='export_products'),
    path('export/sales/', views.export_sales_to_excel, name='export_sales'),
    path('export/achats/', views.export_achats_to_excel, name='export_achats'),

    path('UpdateAchat/<int:num>/', views.UpdateAchat, name='UpdateAchat'),
    path('InsertAchat/', views.InsertAchat, name='InsertAchat'),
    path('DelAchat/<int:num>/', views.DelAchat, name='DelAchat'),
    path('EditAchat/<int:num>/', views.EditAchat, name='EditAchat'),

    path('InsertVentes/', views.InsertVentes, name='InsertVentes'),
    path('EditVentes/<int:num>/', views.EditVentes, name='EditVentes'),
    path('UpdateVentes/<int:num>/', views.updateVentes, name='updateVente'),
    path('DeleteVentes/<int:num>/', views.DelVentes, name='DeleteVente'),

    path('InsertArticle/', views.InsertArticles, name='InsertArticles'),
    path('DeleteArticle/<str:art_id>/', views.DelArticles, name='DeleteArticle'),
    path('EditArticle/<str:art_id>/', views.EditArticles, name='EditArticle'),
    path('UpdateArticle/<str:art_id>/', views.updateArticles, name='updateArticle'),

    path('clients/', views.show_clients_table, name='clients_table'),
    path('InsertClient/', views.InsertClient, name='InsertClient'),
    path('EditClient/<int:client_id>/', views.EditClient, name='EditClient'),
    path('DeleteClient/<int:client_id>/', views.DeleteClient, name='DeleteClient'),

    path('sidebar2/', views.sidebar_view, name='sidebar2'),
]
