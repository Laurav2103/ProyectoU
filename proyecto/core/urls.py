from django.urls import path
from .views import createArticle, home, editArticle, eraseArticle, search_r

urlpatterns = [
    path('', home, name="home"),
    path('createArticle/', createArticle, name="createArticle"),
    path('editArticle/<int:id>/', editArticle, name="editArticle"),
    path('eraseArticle/<int:id>/', eraseArticle, name="eraseArticle"),
    path('search_r/', search_r, name="search_r"),
]
