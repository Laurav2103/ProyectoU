from django.shortcuts import redirect, render
from .models import article
from .forms import ArticleForm
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
        articles = article.objects.filter(nombreArticulo__contains=searched)
        return render(request, 'core/search_r.html', {'searched': searched, 'articles': articles})

    else:
        return render(request, 'core/search_r.html', {})
