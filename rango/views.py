from django.shortcuts import render

from django.http import HttpResponse

from rango.models import Category, Page


def index(request):

    # Query the database for a list of ALL categories currently stored.
    # Order the categories by no. likes in descending order.
    # Retrieve the top 5 only - or all if less than 5.
    # Place the list in our context_dict dictionary
    # that will be passed to the template engine.
    category_list = Category.objects.order_by('-likes')[:5]
    context_dict = {'categories' : category_list}
    return render(request, 'rango/index.html', context=context_dict)

    """
    # Construct a dictionary to pass to the template engine as its context.
    # Note the key boldmessage is the same as {{ boldmessage }} in the template!
    context_dict = {'boldmessage' : "Crunchy, creamy, cookie, candy, cupcake!" }

    # Return a rendered response to send to the client.
    # Note that the first parameter is the template we wish to use.
    return render(request, 'rango/index.html', context=context_dict)
    """


def about(request):

    return render(request, 'rango/about.html', {})
    """return HttpResponse("Rango says here is the <b>About</b> page. <br/> \
         <a href='/rango'>Index</a>") """

