from django.urls import path
from . import views

app_name='polls'
urlpatterns=[
    path('',views.index,name='index'), #This is basically a self-referencing route
    path('<int:question_id>',views.detail,name='detail'), #Passes the question's ID to get the Question & Choices
    path('<int:question_id>/results/',views.results,name='results') #Gets the question & displays its results
]