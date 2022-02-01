from django.shortcuts import redirect, render
from .models import article
from .forms import ArticleForm
from django.db.models import Q
from nltk import SnowballStemmer
import nltk
import spacy
# Create your views here.


def home(request):
    articles = article.objects.all()
    data = {
        'articles': articles
    }
    return render(request, 'core/home.html', data)


def createArticle(request):
    if request.method == 'GET':
        articles = article.objects.all()
        form = ArticleForm()
        data = {
            'form': form
        }
    else:
        form = ArticleForm(request.POST)
        data = {
            'form': form
        }
    if form.is_valid():
        form.save()
        return redirect('home')

    return render(request, 'core/createArticle.html', data)


def editArticle(request, id):
    articles = article.objects.get(id=id)
    if request.method == 'GET':
        form = ArticleForm(instance=articles)
        data = {
            'form': form
        }
    else:
        form = ArticleForm(request.POST, instance=articles)
        data = {
            'form': form
        }
        if form.is_valid():
            form.save()
            return redirect('home')

    return render(request, 'core/createArticle.html', data)


def eraseArticle(request, id):
    articles = article.objects.get(id=id)
    articles.delete()
    return redirect('home')


def search_r(request):
    if request.method == "POST":

        searched = request.POST['searched']
        original = searched
        # Process nlp ---- word searched---------------------------------------------------------
        print(searched)
        nlp = spacy.load('es_core_news_sm')
        doc = nlp(searched)
        spanishstemmer = SnowballStemmer('spanish')
        words = [t.orth_ for t in doc if not t.is_punct | t.is_stop]
        tokens = [t.lower() for t in words if len(t) > 3 and
                  t.isalpha()]
        stems = [spanishstemmer.stem(token) for token in tokens]
        # print(stems)
        # Process nlp ----- camp catalogation------------------------------------------------------
        #catpr = article.objects.get()
        lista_cat = list(article.objects.all())
        #var = article.objects.all()
        # print(lista_cat[2][4])
        obj = article()

        obj.id = 5
        obj.categoria = "hola"
        # print(obj.id)
        for x in range(0, len(lista_cat)):
            # print(lista_cat[x])
            aux = lista_cat[x]
            # print(aux)
            #aux = iter(lista_cat)
            # print(next(aux))
            strA = "".join(map(str, aux))
            # print(strA)
            #aux2 = iter(strA)
            # print(next(aux2))
            doc = nlp(strA)
            spanishstemmer = SnowballStemmer('spanish')
            words = [t.orth_ for t in doc if not t.is_punct | t.is_stop]
            tokens = [t.lower() for t in words if len(t) > 3 and
                      t.isalpha()]
            stemse = [spanishstemmer.stem(token) for token in tokens]
            # print(stemse)

        #articles = article.objects.all()
        articles = article.objects.filter(
            Q(nombreArticulo__icontains=searched) | Q(catalogacion__icontains=searched))  # catalogacion__icontains

        return render(request, 'core/search_r.html', {'searched': searched, 'articles': articles})

    else:
        return render(request, 'core/search_r.html', {})
