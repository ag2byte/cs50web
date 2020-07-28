import markdown2
import random
import re
from django.shortcuts import render, redirect, HttpResponse

from . import util

pagelist = util.list_entries()

# default page


def index(request):
    return render(request, "encyclopedia/index.html", {
        "entries": util.list_entries()
    })

# rendering page content for a title


def wiki(request, title):
    pagelist = util.list_entries()

    if title in pagelist:
        content = util.get_entry(title)

        return render(request, "encyclopedia/page.html", {
            "title": title,
            "content": markdown2.markdown(content)
            # send title and content to HTML
        })
    else:
        return render(request, "encyclopedia/error.html", {
            'error_message': 'Page not found'
        })

# random page


def random_page(request):

    # random no. in [0-len[pagelist]-1]]
    r = random.randint(0, len(pagelist)-1)
    title = pagelist[r]

    return redirect(wiki, title=title)  # redirect to this page

# search


def search(request):
    if request.method == 'POST':
        term = request.POST
        term = term['q']
        searchlist = []

        for page in pagelist:

            if re.search(term.lower(), page.lower()):  # case in sensitive
                searchlist.append(page)
        if len(searchlist) == 0:  # searchlist is empty
            return render(request, "encyclopedia/error.html", {
                'error_message': f'No results found for \'{term}\' '
            })

    return render(request, "encyclopedia/search.html", {
        'entries': searchlist
    })

# new page


def add_page(request):
    if request.method == 'POST':
        title = request.POST.get('title')
        content = request.POST.get('content')
        print(f'title:{title}')
        print(f'content:{content}')
        if title in pagelist:
            return render(request, "encyclopedia/add.html", {
                'available': True
                # page already exists
            })
        else:
            util.save_entry(title, content)
            return redirect(wiki, title=title)
    return render(request, "encyclopedia/add.html", {
        'available': False

    })

# edit markdown


def edit_page(request, title):
    pagecontent = util.get_entry(title)
    if request.method == 'GET':
        return render(request, "encyclopedia/edit.html", {
            'title': title,
            'content': pagecontent
        })
    if request.method == 'POST':
        pagecontent = request.POST.get('newcontent')
        util.save_entry(title, pagecontent)
        return redirect(wiki, title=title)
