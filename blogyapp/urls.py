from django.urls import path
from .import views

app_name = 'blogyapp'
urlpatterns = [
    path("",views.home1,name='home1'), 
    path("index/",views.index,name='index'),   #name is index
    path('topics/<int:topic_id>/', views.topic, name='topic'),
    path('new_topic/', views.new_topic, name='new_topic'),

    path('new_entry/<int:topic_id>/', views.new_entry, name='new_entry'),
    path('edit_entry/<int:entry_id>/', views.edit_entry, name='edit_entry'), # does entry have an id??
    path('edit_topic/<int:topic_id>/', views.edit_topic, name = "edit_topic"),

    path('read/<int:read_id>/',views.read, name = "read"),
    path('delete_entry/<int:entry_id>/', views.delete_entry , name = "delete_entry"),
    path('delete_topic/<int:topic_id>/', views.delete_topic, name = "delete_topic"),

    path('practice/',  views.practice , name=" practice ")

]

 #<a href="{% url 'blogyapp:edit_entry' entry.id %}">Edit entry</a> 