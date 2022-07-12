from django.shortcuts import render
from django import forms
from . import util

class NewSearchForm(forms.Form):
    TITLE = forms.CharField(label = "Search Encyclopedia")

def index(request):
    return render(request, "encyclopedia/index.html", {
        "entries": util.list_entries(), "form":NewSearchForm()
    })

def title(request, TITLE):
    if request.method == "POST":
        form = NewSearchForm(request.POST)
        TITLE = form.data["TITLE"]
    return render(request, "encyclopedia/page.html", {
        "TITLE": TITLE, "get_entry" : util.get_entry(TITLE), "form":NewSearchForm(), "list_entries" : util.list_entries()
    })

def search(request):
    if request.method == "POST":
        form = NewSearchForm(request.POST)
        TITLE = form.data["TITLE"]
        if title(request,TITLE) != None :
            return title(request,TITLE)
        else:
            return render(request, "encyclopedia/index.html", {
                "entries": util.search_entries(TITLE), "form":NewSearchForm()
            })
    #return render(request, "encyclopedia/index.html", {
        #"entries": util.list_entries(), "form":NewSearchForm()
    #})