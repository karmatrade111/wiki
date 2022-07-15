from django.shortcuts import render
from django import forms
from . import util
from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponseRedirect
from django.urls import reverse

@csrf_exempt 

class NewSearchForm(forms.Form):
    TITLE = forms.CharField(label = "Search Encyclopedia")

class CreatePageForm(forms.Form):
    PAGETITLE = forms.CharField(label = "Add a Title")
    PAGECONTENT = forms.CharField(label = "Write Content")

class EditPageForm(forms.Form):
    originalTitle = "CSS"
    EDITPAGETITLE = forms.CharField(label="Edit Title", initial=originalTitle)
    EDITPAGECONTENT = forms.CharField(label = "Edit Content", initial = util.get_entry(originalTitle), widget=forms.Textarea)


def index(request):
    if request.method == "POST":
        form = NewSearchForm(request.POST) 
        TITLE = form.data["TITLE"]
        if util.get_entry(TITLE) != None :
            return title(request, TITLE)
        else:
            return render(request, "encyclopedia/index.html", {
                "entries": util.search_entries(TITLE), "form":NewSearchForm()
            })
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

def newPage(request):
    confirm ="no"
    if request.method == "POST":
        if 'Search' in request.POST:
            form = NewSearchForm(request.POST) 
            TITLE = form.data["TITLE"]
            if util.get_entry(TITLE) != None :
                return title(request, TITLE)
            else:
                return render(request, "encyclopedia/index.html", {
                    "entries": util.search_entries(TITLE), "form":NewSearchForm()
                })
        elif 'Create New Page' in request.POST:
            createPage = CreatePageForm(request.POST)
            PAGETITLE = createPage.data["PAGETITLE"]
            PAGECONTENT = createPage.data["PAGECONTENT"]
            if PAGETITLE not in util.list_entries(): 
                util.save_entry(PAGETITLE, PAGECONTENT)
                confirm = "Submitted"
            else:
                confirm = "This page already exists"
    return render(request, "encyclopedia/newPage.html", {
            "createPage":CreatePageForm(), "form":NewSearchForm(), "confirm":confirm
    })

def edit(request, title):
    content = util.get_entry(title)
    confirm ="no"
    if request.method=="POST":
        editPage = EditPageForm(request.POST)
        PAGETITLE = editPage.data["EDITPAGETITLE"]
        PAGECONTENT = editPage.data["EDITPAGECONTENT"]
        util.save_entry(PAGETITLE, PAGECONTENT)
        confirm ="yes"
        return HttpResponseRedirect(reverse('success', kwargs={'title': title}))
    return render (request, "encyclopedia/edit.html", {
        "title": title, "content": content, "editPage":EditPageForm(), "confirm":confirm
    })

def success(request, title):
    return render (request, "encyclopedia/success.html", {
        "title": title
    })
