# cd desktop/cs50/project_1/wiki
# python3 manage.py runserver

from django.shortcuts import render
from random import *
from . import util, forms, process_markdown as pm
import os, time
from django.shortcuts import redirect, reverse
from django.http import HttpResponseRedirect


def index(request):
    return render(request, "encyclopedia/index.html", {
        "s_form": forms.SearchForm(),
        "entries": util.list_entries()
    })
   
    
# calls and page from its topic name
def wiki(request, filename):
    # get markdown from saved file
    markdown = util.get_entry(filename)
    if markdown == None:
        # if a title is entered on the url and does not exist
        return render(request, "encyclopedia/wiki.html", {
        "s_form": forms.SearchForm(),
        "title": "Page not found"
            })
    dirname = "entries/"
    file = dirname + filename + ".md" 
    # set file datestamp
    ts = "Last modified: %s" % time.ctime(os.path.getmtime(file))
    return render(request, "encyclopedia/wiki.html", {
        "title": filename,
        "s_form": forms.SearchForm(),
        "feedback": ts,
        # passes the markdown as an array
        "markdown": pm.processfile(markdown)
    })

    
# user search, full match, near match, no match
def search(request):
    # result position 0 is flag set to no match
    result = []
    topic_found = "none"
    feedback = "Your search returned no matches."
    if request.method == 'POST':
        form = forms.SearchForm(request.POST)
        if form.is_valid():
            search_value = request.POST['get_search']
            topic_list = util.list_entries()
            for topic in topic_list:
                # for comparison lower used to equalise for the search which is caps sensitive
                # partial match
                if search_value.lower() in topic.lower():
                    result.append(topic)
                    feedback = "Partial matches for your search term"                   
                # exact match returns the page
                if search_value.lower() == topic.lower():
                    topic_found = topic
                    # redirect allows the browser url to reflect accurately args passed in brackets
                    return HttpResponseRedirect(reverse("encyclopedia:wiki", args=[topic_found]) )

    # default - returns a list of results or no results with a create option
    return render(request, "encyclopedia/search.html", {
        "s_form": forms.SearchForm(request.POST),
        "results": result,
        "title": search_value,
        "feedback": feedback 
            })
                    
   
# create a new title, has to test if exists and not save
def create(request, title="Enter Title"):
    feedback = "Title already exists!"
    c = "Place your markdown here"
    flag = False
    if request.method == 'POST':      
        form = forms.ContentForm(request.POST)
        if form.is_valid():
           form_title = form.cleaned_data['title']
		# sets error in new default title not changed
        if form_title == "Enter Title":
            feedback = "A new title is required when saving text"
            flag = True
        if util.get_entry(form_title):
            flag = True
            title = form_title
            
        # tests if placeholder title has been changed
        if flag == True:
            c = form.cleaned_data['content']
            data = { "title": title, "content": c}
            return render(request, "encyclopedia/create.html", {
                "c_form": forms.ContentForm(data),
                "s_form": forms.SearchForm(),
                "feedback": feedback     
                })
        else:
            # save new title and render page
            util.save_entry(request.POST['title'],request.POST['content'])
            # request to open new title through wiki url
            markdown = util.get_entry(request.POST['title'])
            return render(request, "encyclopedia/wiki.html", {
                "title": request.POST['title'],
                "s_form": forms.SearchForm(),
                "markdown": pm.processfile(markdown),
                "feedback": "New title saved"
                })


    # render form to create new entry
    data = { "title": title, "content": c}
    return render(request, "encyclopedia/create.html", {
        "c_form": forms.ContentForm(data),
        "s_form": forms.SearchForm()
		})            

             
#edit an existing page
def edit(request, title):
    # gets the .md file using the utility
    c = util.get_entry(title)
    # if blank document saved, 
    if c == None:
        c = "enter text here"

    # edit existing title 
    data = {"title": title, "content": c }
    return render(request, "encyclopedia/edit.html", {
        "title": title,
        "e_form": forms.EditForm(data),
        "s_form": forms.SearchForm()
		})


# save page and display
def save(request):
    # save title
    if request.method == 'POST':
        title = request.POST['title']
        content = request.POST['content']
        # add blank line to end to fix markdown rendering error 
        content += "\n"
        util.save_entry(title, content)
        # redirect works 
        return HttpResponseRedirect(reverse("encyclopedia:wiki", args=[title]) )


# show a random page, when run it will call encyclopedia using a random page from a list of all 
# so load an array, generate a random number, call the page with that number
def random_page(request):
    #load an array with the pages
    topic_list = util.list_entries()
    min = 0
    max = len(topic_list)-1
    #pick a random number and return the title name
    rn = randint(min, max)
    title = topic_list[rn]
    markdown = util.get_entry(title)
    return render(request, "encyclopedia/wiki.html", {
        "title": title,
        "s_form": forms.SearchForm(),
        "markdown": pm.processfile(markdown),
        "feedback": "random title"
        })
    