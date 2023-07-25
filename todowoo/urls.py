from . import settings
from django.contrib import admin
from django.urls import path
from todo import views
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),

    # Auth
    path('signup/', views.signupuser, name='signupuser'),
    path('logout/', views.logoutuser, name='logoutuser'),
    path('login/', views.loginuser, name='loginuser'),

    # Todos
    path('', views.home, name='home'),
    path('current/', views.currenttodos, name='currenttodos'),
    path('create/', views.createtodo, name='createtodo'),
    path('create/upload/<int:todo_pk>', views.todo_file, name='todo_file'),
    path('completed/', views.completedtodos, name='completedtodos'),
    path('todo/<int:todo_pk>', views.viewtodo, name='viewtodo'),
    path('todo/<int:todo_pk>/complete>', views.completetodo, name='completetodo'),
    path('todo/<int:todo_pk>/completed', views.viewcompletedtodo, name='viewcompletedtodo'),
    path('todo/<int:todo_pk>/delete', views.deletetodo, name='deletetodo'),
]

urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
