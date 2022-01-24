from django.core.files.storage import default_storage
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django import forms
from django.urls import reverse

import markdown
import random
import secrets

from . import util

class NewEntryForm(forms.Form):
    title = forms.CharField(label='Title:')
    content = forms.CharField(widget=forms.Textarea,label='Markdown content:')
    edit_mode = forms.BooleanField(initial=False,required=False,widget=forms.HiddenInput())

def index(request):
    return render(request, "encyclopedia/index.html", {
        "entries": util.list_entries()
    })

def entry(request,title):
    page_content = util.get_entry(title)
    if page_content is None:
        return render(request, 'encyclopedia/notfound.html',{
            'title':title
        })
    else:
        return render(request, 'encyclopedia/entry_page.html',{
            'title':title,
            'content':markdown.markdown(page_content),
        })

def search_entry(request):
    value = request.GET.get('q','')
    if util.get_entry(value):
        return HttpResponseRedirect(reverse('entry',kwargs={'title':value}))
    else:
        empty=False
        matching_entries = list(filter(lambda title: value.lower() in title.lower(), util.list_entries()))
        if len(matching_entries)==0:
            emptry = True
        return render(request, "encyclopedia/index.html", {
            "entries": matching_entries,
            "search":True,
            "value":value,
            "empty":empty
        })


def new_entry(request):
    if request.method=="POST":
        form = NewEntryForm(request.POST)
        if form.is_valid():
            title = form.cleaned_data['title']
            content = form.cleaned_data['content']
            if (util.get_entry(title) is None or form.cleaned_data['edit_mode']==True):
                util.save_entry(title,content)
                return HttpResponseRedirect(reverse('entry',kwargs={'title':title}))
            else:
                return render(request,"encyclopedia/new_entry.html", {
                        "form":form,
                        "existing":True,
                        "title":title
                    })
        else:
            return render(request,"encyclopedia/new_entry.html", {
                "form":form,
                "existing":False
            })
    else:
        return render(request,"encyclopedia/new_entry.html", {
            "form":NewEntryForm(),
            "existing":False
        })

def edit_page(request,title):
    entry = util.get_entry(title)
    if entry is None:
        return render(request,'encyclopedia/notfound.html',{
            'title':title,
        })
    else:
        form = NewEntryForm()
        form.fields['title'].initial = title
        form.fields['title'].widget = forms.HiddenInput()
        form.fields['content'].initial = entry
        form.fields['edit_mode'].initial = True
        return render(request,'encyclopedia/new_entry.html',{
            'form':form,
            'edit_mode':True,
            'title':title
        })

def random_page(request):
    entries = util.list_entries()
    random_entry = secrets.choice(entries)

    return HttpResponseRedirect(reverse('entry',kwargs={'title':random_entry}))


