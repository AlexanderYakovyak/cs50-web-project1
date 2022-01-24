from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("wiki/<str:title>",views.entry,name="entry"),
    path("wiki/<str:title>/edit_page",views.edit_page,name='edit_page'),
    path('search_entry',views.search_entry,name='search_entry'),
    path('random_page',views.random_page,name='random_page'),
    path("new_entry",views.new_entry,name="new_entry")

]
