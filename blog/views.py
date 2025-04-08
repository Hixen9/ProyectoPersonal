from django.shortcuts import render
from blog.models import Categoria,Post

def blog(request):

    posts = Post.objects.all()
    return render(request,"blog/blog.html",{"posts":posts})

def categoria(request, categoria_id):
    categoria = Categoria.objects.get(id = categoria_id)
    posts = Post.objects.filter(categorias = categoria)
    seleccionarPost = Post.objects.all()
    return render(request,"blog/categorias.html",{"categorias":categoria,"posts":posts,"all":seleccionarPost})
