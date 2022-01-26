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
        # Process nlp
        logging.info(searched)
        nlp = spacy.load('es_core_news_sm')
        doc = nlp(searched)
        spanishstemmer = SnowballStemmer('spanish')
        words = [t.orth_ for t in doc if not t.is_punct | t.is_stop]
        tokens = [t.lower() for t in words if len(t) > 3 and
                  t.isalpha()]
        stems = [spanishstemmer.stem(token) for token in tokens]
        logging.debug(stems)
        #articles = article.objects.all()
        articles = article.objects.filter(
            Q(nombreArticulo__icontains=searched) | Q(catalogacion__icontains=searched))
        return render(request, 'core/search_r.html', {'searched': searched, 'articles': articles})

    else:
        return render(request, 'core/search_r.html', {})
