# cd desktop/cs50/project_1/wiki
# python3 manage.py runserver

from django.shortcuts import render
from random import *
from . import util
from . import forms
from . import process_markdown as pm


def index(request):
    return render(request, "encyclopedia/index.html", {
        "s_form": forms.SearchForm(),
        "entries": util.list_entries()
    })
   
    
# calls and page from its topic name
def wiki(request, title):
    # get markdown
    markdown = util.get_entry(title)
    #convert to html
    return render(request, "encyclopedia/wiki.html", {
        "s_form": forms.SearchForm(),
        "markdown": pm.processfile(markdown.splitlines(True))
    })

    
# user search, full match, near match, no match
def results(request):
    # result position 0 is flag set to no match
    result = []
    topic_found = "none"
    flag = 0
    fb = "no matches"
    if request.method == 'POST':
        form = forms.SearchForm(request.POST)
        if form.is_valid():
            r_value = request.POST['get_search']
            topic_list = util.list_entries()
            print(topic_list)
            for topic in topic_list:
                # partially or all match. lower used to equalise for the search which is caps sensitive
                if r_value.lower() in topic.lower():
                    print("partial")
                    flag = 1
                    result.append(topic)
                    print(result)
                    fb = "partial matches"                   
                # exact match
                if r_value.lower() == topic.lower():
                    print("search exact match")
                    topic_found = topic
                    # call wiki function when topic found
                    return wiki(request, topic_found)
    # returns a list of results or no results
    print("search no full or partial match")

    return render(request, "encyclopedia/results.html", {
        "s_form": forms.SearchForm(request.POST),
        "results": result,
        "type": flag,
        "title": r_value,
        "feedback": fb 
            })
                    
   
# create a new title, has to test if exists and not save
def create(request):
    t = "Enter Title"
    c = "Place your markdown here"
    if request.method == 'POST':      
        form = forms.ContentForm(request.POST)
        flag = util.get_entry(request.POST['title'])   
		# if title exists return to form with input
        if request.POST['title'] == "Enter Title":
            flag = True
        if flag :
            t = request.POST['title']
            c = request.POST['content']
            data = { "title": t, "content": c}
            print("title already exists")
            return render(request, "encyclopedia/create.html", {
                "c_form": forms.ContentForm(data),
                "s_form": forms.SearchForm(),
                "feedback": "title already exists"     
                })
        else:
            #save new title and render page
            print("save new title")
            util.save_entry(request.POST['title'],request.POST['content'])
            return render(request, "encyclopedia/wiki.html", {
                "title": request.POST['title'],
                "s_form": forms.SearchForm(),
                "markdown": util.get_entry(request.POST['title']),
                "feedback": "title saved"
                })
    #render form
    data = { "title": t, "content": c}
    return render(request, "encyclopedia/create.html", {
        "c_form": forms.ContentForm(data),
        "s_form": forms.SearchForm()
		})            
                
#edit page
def edit(request, title = "Enter Title"):
    if request.method == 'POST':
        form = forms.ContentForm(request.POST)
        flag = util.get_entry(request.POST['title'])   
		# if title exists return to form with input
        util.save_entry(request.POST['title'],request.POST['content'])
        print("save new title")
        #render the page after it is saved
        return render(request, "encyclopedia/wiki.html", {
            "title": request.POST['title'],
            "s_form": forms.SearchForm(),
            "markdown": util.get_entry(request.POST['title']),
            "feedback": "saved"
             })
    c = util.get_entry(title)
    if c == None:
        c = "enter text here"
    data = { "title": title, "content": c }
    print("edit title")
    return render(request, "encyclopedia/edit.html", {
        "c_form": forms.ContentForm(data),
        "s_form": forms.SearchForm()
		})
    


# show a random page, when run it will call encyclopedia using a random page from a list of all 
# so load an array, generate a random number, call the page with that number
def random_page(request):
    #load an array with the pages
    topic_list = util.list_entries()
    print(topic_list)
    min = 0
    max = len(topic_list)-1
    print(max)
    #pick a random number and return the title name
    rn = randint(min, max)
    title = topic_list[rn]
    return wiki(request, title)
    