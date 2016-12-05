# Create your views here.
from django.shortcuts import render
import json
from django.forms.models import modelform_factory
from django.views.generic import View
import sys
from django.http import HttpResponse
def main(request):
    return render(request, "main.html")
def getJson(filename):
    file = open(filename, "r")
    authors = json.load(file)
    return authors
class Author_id(View):
    def get(self, request, path):
        authors = getJson("authors.json")
        author = {}
        for a in authors:
            if a['id'] == int(path):
                author = a
                break

        return render(request, "author.html", {'author': author})

def Authors(request):
    authors = getJson("authors.json")
    return render(request, "all.html", {'authors': authors})

