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
        # Process nlp ---- word searched---------------------------------------------------------
        # print(searched)
        nlp = spacy.load('es_core_news_sm')
        doc = nlp(searched)
        spanishstemmer = SnowballStemmer('spanish')
        words = [t.orth_ for t in doc if not t.is_punct | t.is_stop]
        tokens = [t.lower() for t in words if len(t) > 3 and
                  t.isalpha()]
        stems = [spanishstemmer.stem(token) for token in tokens]
        print(stems)
        # Process nlp ----- camp catalogation------------------------------------------------------
        lista_cat = list(article.objects.all())

        # print(obj.id)
        for x in range(0, len(lista_cat)):  # For process the list
            aux = lista_cat[x]
            # print(aux)
            #aux = iter(lista_cat)
            # print(next(aux))
            strA = "".join(map(str, aux))  # Convert to string
            # print(strA)
            #aux2 = iter(strA)
            # print(next(aux2))
            doc = nlp(strA)  # Use to spacy
            spanishstemmer = SnowballStemmer('spanish')
            words = [t.orth_ for t in doc if not t.is_punct | t.is_stop]
            tokens = [t.lower() for t in words if len(t) > 3 and
                      t.isalpha()]
            stemse = [spanishstemmer.stem(token)
                      for token in tokens]  # word process
            print(stemse)
            """for i in range(0, len(stemse)):
                aux1 = stemse[i]
                print(aux1)"""
            """p = article(catalog_process=stemse)
            p.save()"""
            # ------------Convert to string -----------
            #strC = "".join(map(str, stemse))
            # print(strC)
            # saveField(request, id=, strC)

            # _----------llenado campo---------------------------------------
            # article.objects.update_or_create('catalogacion')
            # article.objects.get(nombreArt="hola")

            # obj=article.objects.create(val=id)
            # article.objects.filter(pk=obj.pk).update(vcatalog_process=strC)
            # print(article.objects.get(pk=16))
            # print(article.id)

            # article.save(update_fields=['catalog_process'])
            #p.catalog_process = strC
            # p.save(update_fields=['catalog_process'])
            # article.save(self=article, force_insert=false, force_update=true,
            #             using=article, update_fields=p.catalog_process(strC))
            #articles = article.objects.get(id=id)
            #articles = article(catalog_process=strC)
            # p.id
            # articles.save()
            """ to_edit = article.objects.get(id=13)
            to_edit.catalog_process = strC
            to_edit.save()"""
        #articles = article.objects.all()
        auxbus = searched
        searched = stems
        articles = article.objects.filter(
            Q(nombreArticulo__icontains=searched) | Q(catalog_process__icontains=searched) | Q(nombreArticulo__icontains=auxbus) | Q(catalogacion__icontains=auxbus))  # catalogacion__icontains

        return render(request, 'core/search_r.html', {'searched': searched, 'articles': articles})

    else:
        return render(request, 'core/search_r.html', {})
