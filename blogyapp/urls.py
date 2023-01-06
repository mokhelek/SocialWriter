from django.urls import path
from .import views

app_name = 'blogyapp'
urlpatterns = [
    path("",views.home1,name='home1'),
    path("following/",views.following,name='following'),
    path("popular/",views.popular,name='popular'),
     

    path('new_entry/<int:profile_id>/', views.new_entry, name='new_entry'),
    path('edit_entry/<int:entry_id>/', views.edit_entry, name='edit_entry'), # does entry have an id??
   

    path('read/<int:read_id>/',views.read, name = "read"),
    path('delete_entry/<int:entry_id>/', views.delete_entry , name = "delete_entry"),

    # path('dashboard/',  views.dashboard , name="dashboard"),
   

    path('profile_detail/<int:profile_id>/', views.profile_detail, name='profile_detail'), 
    path('follow_unfollow/<int:profile_id>/', views.follow_unfollow, name='follow_unfollow'), 
    
    path('like_unlike/<int:entry_id>/', views.like_unlike, name='like_unlike'), 
    
    path('bookmark/<int:entry_id>/', views.bookmark, name='bookmark'),
    
    path('my_bookmarks/<int:profile_id>/', views.my_bookmarks, name='my_bookmarks'),
    
    path('user_entries/', views.user_entries, name='user_entries'),
    
    path('publish_or_unpublish/<int:entry_id>/', views.publish_or_unpublish, name='publish_or_unpublish'),
    
    

]
