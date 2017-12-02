import os
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'tango_django.settings')

import django
django.setup()
from rango.models import Category, Page

def populate():

    # First, we will create lists of dictionaries containing the pages
    # we want to add into each category.
    # Then we will create a dictionary of dictionaries for our categories.
    # This might seem a little bit confusing, but it allows us to iterate
    # through each data structure, and add the data to our models.
    python_pages = [
        {"title": "Official Python Tutorial", "url":"http://docs.python.org/2/tutorial/", "views": 32},
        {"title":"How to Think like a Computer Scientist", "url":"http://www.greenteapress.com/thinkpython/", "views": 16},
        {"title": "Principales diferencias entre Python 2 y 3 con ejemplos", "url": "https://www.pythonmania.net/es/2016/02/29/las-principales-diferencias-entre-python-2-y-3-con-ejemplos/", "views": 21},
        {"title":"Learn Python in 10 Minutes", "url":"http://www.korokithakis.net/tutorials/python/", "views": 55},  ]

    django_pages = [
        {"title":"Official Django Tutorial",
            "url":"https://docs.djangoproject.com/en/1.9/intro/tutorial01/", "views": 14},
        {"title":"Django Girls Tutorial",
            "url":"https://www.gitbook.com/book/djangogirls/djangogirls-tutorial/details", "views": 23},
        {"title":"Django Rocks",
            "url":"http://www.djangorocks.com/" , "views": 56},
        { "title":"How to Tango with Django",
            "url":"http://www.tangowithdjango.com/", "views": 12 } ]

    other_pages = [
        { "title":"Bottle", "url":"http://bottlepy.org/docs/dev/", "views": 25},
        { "title":"Flask", "url":"http://flask.pocoo.org", "views": 67} ]

    cats = {"Python": {"pages": python_pages, "views": 128, "likes": 64},
            "Django": {"pages": django_pages, "views": 64, "likes": 32},
            "Other Frameworks": {"pages": other_pages, "views": 14, "likes": 32},
            "Pascal": {"pages": [], "views": 8, "likes": 6},
            "Perl": {"pages": [], "views": 14, "likes": 12},
            "Php": {"pages": [], "views": 22, "likes": 34},
            "Prolog": {"pages": [], "views": 11, "likes": 13},
            "Programming": {"pages": [], "views": 52, "likes": 65},

            }

    # if you want to add more catergories or pages, add them to the dictionaries above
    # The code below goes through the cats dictionary, then adds each category,
    # and then adds all the associated pages for that category
    # if you are using Python 2.x then use cats.iteritems() see
    # http://docs.quantifiedcode.com/python-anti-patterns/readability/not_using_items_to_iterate_over_a_dictionary.html
    # for more information about using items() and how to iterate over a dictionary properly

    # Using the .items returns the key and the value. In this case the key is "Python", "Django" or "Other Frameworks" and the value (cat_data) is the corresponding dictionary in cats.
    for cat, cat_data in cats.items():
        # c = add_cat(cat)
        # Updated the population script to pass through the specific values for views and likes
        c = add_cat(cat, cat_data["views"], cat_data["likes"])
        for p in cat_data["pages"]:
            add_page(c, p["title"], p["url"], p["views"])

    # Print out what we have added to the user.
    for c in Category.objects.all():
        for p in Page.objects.filter(category=c):
            print("- {0} - {1}".format(str(c), str(p)))


def add_page(cat, title, url, views=0):
    p = Page.objects.get_or_create(category=cat, title=title)[0]
    p.url=url
    p.views=views
    # we need to save the changes we made!!
    p.save()
    return p

def add_cat(name, views=0, likes=0):
    c = Category.objects.get_or_create(name=name)[0]
    c.views=views
    c.likes=likes
    c.save()
    return c

# Start execution here!
if __name__ == '__main__':
    print("Starting Rango population script...")
populate()

