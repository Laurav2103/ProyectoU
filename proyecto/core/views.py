from zlib import DEF_BUF_SIZE
import spacy
import nltk
from nltk import SnowballStemmer
import unicodedata
import requests
from bs4 import BeautifulSoup
from django.db.models import Q
from .forms import ArticleForm
from .models import article
from re import X, search
import django
from django.shortcuts import redirect, render
from sqlalchemy import false, true
import os
os.environ.setdefault("DJANGO_SETTINGS_MODULE", ".settings")
django.setup()
#from proyecto.core.admin import articleResourse
# Create your views here.


def home(request):
    articles = article.objects.all()

    data = {
        'articles': articles
    }
    """p = article.save()
    id = p.id
    print(id)
    nlpField(id)"""

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
        # p = article()
        p = form.save()
        id = p.id
        nlpField(id)
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
            p = form.save()
            id = p.id
            nlpField(id)
            return redirect('home')

    return render(request, 'core/createArticle.html', data)


def eraseArticle(request, id):
    articles = article.objects.get(id=id)

    articles.delete()
    # id=id
    return redirect('home')


def search_r(request):
    if request.method == "POST":

        nlpField(16)

        searched = request.POST['searched']
        # Process nlp ------------------ Word searched-------------------------------------------
        # print(searched)

        # -------------Sinonimos para searched---------------------------------------------------------
        """for x in range(0, len(lemmas)):
            word = lemmas[x]
            sin = synonyms(word)
            print(sin)"""

        # --------------Quita acentos---------------------------------------------------------------------
        trans_tab = dict.fromkeys(map(ord, u'\u0301\u0308'), None)
        searched1 = unicodedata.normalize(
            'NFKC', unicodedata.normalize('NFKD', searched).translate(trans_tab))
        # print(searched1)
        # --------------Process spacy (nltk stemmming)---------------------------------------------------
        nlp = spacy.load('es_core_news_sm')
        doc = nlp(searched1)
        spanishstemmer = SnowballStemmer('spanish')
        words = [t.orth_ for t in doc if not t.is_punct | t.is_stop]
        tokens = [t.lower() for t in words if len(t) > 3 and
                  t.isalpha()]  # frase limpia y tokenizada sin words stop
        stems = [spanishstemmer.stem(token) for token in tokens]
        strS = ", ".join(map(str, stems))  # string estemizada

        # -------------Procces spacy (lemmatize)--------------------------------------------------------
        # string aux tokenizada sin words stop para lemmatizar
        Saux = " ".join(map(str, tokens))
        doc1 = nlp(Saux)
        lemmas = [tok.lemma_.lower() for tok in doc1]
        # print(lemmas)
        strL = ", ".join(map(str, lemmas))  # string lemmatizada
        # print(strL)

        # Process nlp ----------------- Camp catalogation spacy stems------------------------------------
        #lista_cat = list(article.objects.all())
        campo = article.catalogacion
        # print(campo)
        q = article()
        cat = article._meta.get_field('catalogacion')
        este2 = getattr(q, 'catalogacion')
        lista_cat = list(este2)
        # print(lista_cat)
        for x in range(0, len(lista_cat)):  # For process the list

            aux = lista_cat[x]
            print(aux)
            aux = iter(lista_cat)
            # print(next(aux))
            # -------------------Quita acentos al campo----------------------------------------------------------
            str1 = "".join(map(str, aux))
            strA = unicodedata.normalize(
                'NFKC', unicodedata.normalize('NFKD', str1).translate(trans_tab))
            # print(strA)
            # ------------------------Process spacy (nltk stemmming)----------------------
            doc = nlp(strA)  # Use to spacy
            spanishstemmer = SnowballStemmer('spanish')
            words = [t.orth_ for t in doc if not t.is_punct |
                     t.is_stop]  # eliminate stop words
            tokens = [t.lower() for t in words if len(t) > 3 and
                      t.isalpha()]
            stemse = [spanishstemmer.stem(token)
                      for token in tokens]  # stemming with spanishtemmer nltk
            strC = "".join(map(str, stemse))  # string stemizada
            print(strC)
            Saux2 = " ".join(map(str, tokens))  # string axu para lematizar
            doc2 = nlp(Saux2)
            lemmas2 = [tok.lemma_.lower() for tok in doc2]
            # print(lemmas2)
            strD = "".join(map(str, lemmas2))  # Lemmatization Spacy
            print(strD)
            """p = article(catalog_process=stemse)
            p.save()"""
            # ------------Convert to string -----------

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
        #syn = 'causa' 'motivo' 'adquirir' 'obtener' 'conseguir' 'mercar' 'comerciar' 'pospago'
        syn = 'causa motivo adquirir obtener conseguir mercar comerciar pospago'
        print(searched)
        print(strS)
        print(strL)

        articles = article.objects.filter(Q(catalog_process__icontains=strS) |
                                          Q(nombreArticulo__icontains=searched) |
                                          Q(titleProcess__icontains=strS) | Q(catalogacion__icontains=strL))  # catalogacion__icontains

        return render(request, 'core/search_r.html', {'searched': searched, 'articles': articles})

        # ----------------------------FOR SYNONYMS-------------------------
        """cont = 0
        for i in range(0, len(lemmas)):
            match = syn.find(lemmas[i])
            if match != -1:
                cont = cont+1
        if cont == len(lemmas):
            print("SI ESTÁ BOLUDO")
        else:
            print("KYC")"""

    else:
        return render(request, 'core/search_r.html', {})


def synonyms(word):

    url = 'http://www.wordreference.com/sinonimos/'
    #print("OLA CMO ESTAS")
    #url = 'http://www.sinonimosonline.com/'
    enlace = word
    # print(enlace)
    buscar = url+enlace
    resp = requests.get(buscar)
    bs = BeautifulSoup(resp.text, 'lxml')
    lista = bs.find_all(class_='trans clickable')
    aux2 = []
    aux = []

    for sin in lista:
        sino = sin.find_all('li')
        # print(sino)
        aux = sino[0].next_element
    strx = "".join(map(str, aux))
    # print(strx)
    #list_aux = list(strx)
    # print(list_aux)

    return strx


def nlpWord(searched):

    # --------------Quita acentos---------------------------------------------------------------------
    trans_tab = dict.fromkeys(map(ord, u'\u0301\u0308'), None)
    searched1 = unicodedata.normalize(
        'NFKC', unicodedata.normalize('NFKD', searched).translate(trans_tab))
    # print(searched1)
    # --------------Process spacy (nltk stemmming)---------------------------------------------------
    nlp = spacy.load('es_core_news_sm')
    doc = nlp(searched1)
    spanishstemmer = SnowballStemmer('spanish')
    words = [t.orth_ for t in doc if not t.is_punct | t.is_stop]
    tokens = [t.lower() for t in words if len(t) > 3 and
              t.isalpha()]  # frase limpia y tokenizada sin words stop
    stems = [spanishstemmer.stem(token) for token in tokens]
    strS = ", ".join(map(str, stems))  # string estemizada

    # -------------Procces spacy (lemmatize)--------------------------------------------------------
    # string aux tokenizada sin words stop para lemmatizar
    Saux = " ".join(map(str, tokens))
    doc1 = nlp(Saux)
    lemmas = [tok.lemma_.lower() for tok in doc1]
    # print(lemmas)
    strL = ", ".join(map(str, lemmas))  # string lemmatizada
    # print(strL)

    return strS, strL


def nlpField(id):
    print("OLA")
    print(id)

    articles = article.objects.get(id=id)

    print(articles.nombreArticulo)

    # ----------------Procesado del titulo----------------------------------------------------------
    # --------------Quita acentos---------------------------------------------------------------------
    trans_tab = dict.fromkeys(map(ord, u'\u0301\u0308'), None)
    procesada = unicodedata.normalize(
        'NFKC', unicodedata.normalize('NFKD', articles.nombreArticulo).translate(trans_tab))
    # print(searched1)
    print(procesada)
    nlp = spacy.load('es_core_news_sm')
    doc = nlp(procesada)  # Use to spacy
    spanishstemmer = SnowballStemmer('spanish')
    words = [t.orth_ for t in doc if not t.is_punct |
             t.is_stop]  # eliminate stop words
    tokens = [t.lower() for t in words if len(t) > 3 and
              t.isalpha()]
    stemse = [spanishstemmer.stem(token)
              for token in tokens]  # stemming with spanishtemmer nltk

    strT = ", ".join(map(str, stemse))  # string stemizada
    print(strT)
    articles.titleProcess = strT
    articles.save()
    # ----------------Procesado de Catalogación----------------------------------------------------------
    # --------------Quita acentos---------------------------------------------------------------------
    trans_tab = dict.fromkeys(map(ord, u'\u0301\u0308'), None)
    procesada = unicodedata.normalize(
        'NFKC', unicodedata.normalize('NFKD', articles.catalogacion).translate(trans_tab))
    # print(searched1)
    print(procesada)
    doc = nlp(procesada)  # Use to spacy
    spanishstemmer = SnowballStemmer('spanish')
    words = [t.orth_ for t in doc if not t.is_punct |
             t.is_stop]  # eliminate stop words
    tokens = [t.lower() for t in words if len(t) > 3 and
              t.isalpha()]
    stemse = [spanishstemmer.stem(token)
              for token in tokens]  # stemming with spanishtemmer nltk

    strT = ", ".join(map(str, stemse))  # string stemizada
    print(strT)
    articles.catalog_process = strT
    articles.save()

    """fields = article._meta.get_fields()
    title = article._meta.get_field('nombreArticulo')
    p = article()
    este = getattr(p, 'nombreArticulo')"""

    """lista_tit = list(este)
    listaFin = []
    for x in range(0, len(lista_tit)):  # For process the list
            aux = lista_tit[x]
            print(aux)
            aux = iter(lista_tit)
            # print(next(aux))
            # -------------------Quita acentos al campo----------------------------------------------------------
            str1 = "".join(map(str, aux))  # Convert to string
            strA = unicodedata.normalize(
                'NFKC', unicodedata.normalize('NFKD', str1).translate(trans_tab))  # quitar tildes
            # print(strA)
            # ------------------------Process spacy (nltk stemmming)----------------------
            doc = nlp(strA)  # Use to spacy
            spanishstemmer = SnowballStemmer('spanish')
            words = [t.orth_ for t in doc if not t.is_punct |
                     t.is_stop]  # eliminate stop words
            tokens = [t.lower() for t in words if len(t) > 3 and
                      t.isalpha()]
            stemse = [spanishstemmer.stem(token)
                      for token in tokens]  # stemming with spanishtemmer nltk
            listaFin = stemse
        strT = "".join(map(str, listaFin))  # string stemizada
        # print(strT)"""
