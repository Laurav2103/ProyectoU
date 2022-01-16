from django.urls import path
from .views import createArticle, home, editArticle, eraseArticle

urlpatterns = [
    path('', home, name="home"),
    path('createArticle/', createArticle, name="createArticle"),
    path('editArticle/<int:id>/', editArticle, name="editArticle"),
    path('eraseArticle/<int:id>/', eraseArticle, name="eraseArticle"),
]
