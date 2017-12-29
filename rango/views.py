from django.shortcuts import render, redirect

from django.http import HttpResponse, HttpResponseRedirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.core.urlresolvers import reverse

from datetime import datetime

from rango.models import Category, Page, UserProfile
from rango.forms import CategoryForm, PageForm, UserProfileForm # UserForm
from rango.bing_search import run_query

from registration.backends.simple.views import RegistrationView
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib.auth.forms import PasswordChangeForm


# A helper method
def get_server_side_cookie(request, cookie, default_val=None):
    val = request.session.get(cookie)
    if not val:
        val = default_val
    return val


def visitor_cookie_handler(request):

    # counter
    visits = int(get_server_side_cookie(request, 'visits', 1))

    last_visit_cookie = get_server_side_cookie(request, 'last_visit', str(datetime.now()))
    last_visit_time = datetime.strptime(last_visit_cookie[:-7], '%Y-%m-%d %H:%M:%S')

    # If it's been more than a day since the last visit...
    if (datetime.now() - last_visit_time).seconds > 0:
        visits = visits + 1
        #update the last visit cookie now that we have updated the count
        request.session['last_visit'] = str(datetime.now())
    else:
        visits = 1
        # set the last visit cookie
        request.session['last_visit'] = last_visit_cookie
    # update/set the visits cookie
    request.session['visits'] = visits


def index(request):

    request.session.set_test_cookie()

    # Query the database for a list of ALL categories currently stored.
    # Order the categories by no. likes in descending order.
    # Retrieve the top 5 only - or all if less than 5.
    # Place the list in our context_dict dictionary
    # that will be passed to the template engine.
    category_list = Category.objects.order_by('-likes')[:5]
    page_list = Page.objects.order_by('-views')[:5]

    context_dict = {'categories' : category_list, 'pages' : page_list}

    # Call function to handle the cookies
    visitor_cookie_handler(request)
    context_dict['visits'] = request.session['visits']

    response = render(request, 'rango/index.html', context_dict)
    return response


def about(request):

    """if request.session.test_cookie_worked():
        print("TEST COOKIE WORKED!")
        request.session.delete_test_cookie()"""
    visitor_cookie_handler(request)
    context_dict = {}
    context_dict['visits'] = request.session['visits']
    return render(request, 'rango/about.html', context_dict)


def search(request):

    result_list = []
    if request.method == 'POST':
        query = request.POST['query'].strip() # strip remove the \n from the end of string
        if query:
            result_list = run_query(query)
    return render(request, 'rango/search.html', {'result_list': result_list})



def show_category(request, category_name_slug):

    context_dict = {}

    try:
        category = Category.objects.get(slug=category_name_slug)

        # Retrieve all of the associated pages.
        # Note that filter() will return a list of page objects or an empty list
        pages = Page.objects.filter(category=category)

        # Adds our results list to the template context under name pages.
        context_dict['pages'] = pages

        # Add the category object from the database to the context dictionary.
        # We'll use this in the template to verify that the category exists.
        context_dict['category'] = category
    except Category.DoesNotExist:

        # We get here if we didn't find the specified category.
        # Don't do anything -
        # the template will display the "no category" message for us.
        context_dict['category'] = None
        context_dict['pages'] = None


    # ESTO ESTABA COMENTADO
    # create a default query based on the category name
    # to be shown in the search box
    """context_dict['query'] = category.name
    print("dentro de SHOW CATEGORYttttt.............")

    result_list = []
    if request.method == 'POST':

        query = request.POST['query'].strip()
        if query:
            # Run our Webhose function to get the results list!

            result_list = run_query(query)
            context_dict['query'] = query
    context_dict['result_list'] = result_list

    return render(request, 'rango/category.html', context_dict) """

    # HASTA AQUÍ COMENTADO

    # OJO, COMPROBAR PORQUE SE REPITE EL REENVIO DEL FORMULARIO
    #return render(request, 'rango/category.html', context_dict)

    result_list = []
    if request.method == 'POST':
        context_dict['query'] = category.name
        query = request.POST['query'].strip()
        if query:
            # Run our Webhose function to get the results list!

            result_list = run_query(query)
            context_dict['query'] = query
        context_dict['result_list'] = result_list

    return render(request, 'rango/category.html', context_dict)



@login_required
def add_category(request):
    form = CategoryForm()

    # A HTTP POST
    if request.method == 'POST':
        form = CategoryForm(request.POST)

        # is a valid Form?
        if form.is_valid():

            # Save the category to the db
            category = form.save(commit=True)
            print(category, category.slug)
            # Now that the category is saved
            # We could give a confirmation message
            # But since the most recent category added is on the index page
            # Then we can direct the user back to the index page.
            return index(request)
        else:
            # The supplied form contained errors - just print them to the terminal.
            print(form.errors)

    # Will handle the bad form, new form, or no form supplied cases.
    # Render the form with error messages (if any).
    return render(request, 'rango/add_category.html', {'form': form})



@login_required
def add_page(request, category_name_slug):

    try:
        category = Category.objects.get(slug=category_name_slug)
    except Category.DoesNotExist:
        category = None

    form = PageForm()
    if request.method == 'POST':
        form = PageForm(request.POST)
        if form.is_valid():
            if category:
                page = form.save(commit=False)
                page.category = category
                page.views = 0
                page.save()
            print(page.url)
            print(page.title)
            print("Dentro de add_page.........................................................")
            return show_category(request, category_name_slug)
        else:

            print (form.errors)
    context_dict = {'form': form, 'category': category}
    print(context_dict)
    return render(request, 'rango/add_page.html', context_dict)


"""def register(request):
    # A boolean value for telling the template
    # whether the registration was successful.
    # Set to False initially. Code changes value to
    # True when registration succeeds.
    registered = False

    if request.method == 'POST':
        # Attempt to grab information from the raw form information of both
        user_form = UserForm(data=request.POST)
        profile_form = UserProfileForm(data=request.POST)

        if user_form.is_valid() and profile_form.is_valid():
            # Save the user's form data to the database.
            user = user_form.save()

            # Hash the password with the set_password method.
            # Once hashed, we can update the user object.
            user.set_password(user.password)
            user.save()

            # Now sort out the UserProfile instance.
            # Since we need to set the user attribute ourselves,
            # we set commit=False. This delays saving the model
            # until we're ready to avoid integrity problems.
            profile = profile_form.save(commit=False)
            profile.user = user

            # If the user provided a profile picture, we need to get it from the
            # input form and put it in the UserProfile model.
            if 'picture' in request.FILES:
                profile.picture = request.FILES['picture']
                profile.save()

                # Update our variable to indicate that the template
                # registration was successful.
                registered = True
            else:
                # Invalid form or forms - mistakes or something wrong
                # Print problems to the terminal
                print(user_form.errors, profile_form.errors)
    else:
        # Not a HTTP POST, so we render our form using two ModelForm instances.
        # These forms will be blank, ready for user input.
        user_form = UserForm()
        profile_form = UserProfileForm()

    # Render the template depending on the context
    return render(request, 'rango/register.html',
                                    {'user_form': user_form,
                                        'profile_form': profile_form,
                                        'registered': registered})

"""

@login_required
def register_profile(request):
    form = UserProfileForm()
    if request.method == 'POST':
        form = UserProfileForm(request.POST, request.FILES)
        if form.is_valid():
            user_profile = form.save(commit=False)
            user_profile.user = request.user
            user_profile.save()

            #return redirect('index')
            return HttpResponseRedirect(reverse('index'))
        else:
            print(form.errors)

    context_dict = {'form':form}

    return render(request, 'rango/profile_registration.html', context_dict)



class RangoRegistrationView(RegistrationView):
    def get_success_url(self, user):
        return reverse('register_profile')


@login_required
def profile(request, username):
    try:
        user = User.objects.get(username=username)
    except User.DoesNotExist:
        return redirect('index')

    userprofile = UserProfile.objects.get_or_create(user=user)[0]
    form = UserProfileForm({'website': userprofile.website, 'picture': userprofile.picture})

    if request.method == 'POST':
        form = UserProfileForm(request.POST, request.FILES, instance=userprofile)
        if form.is_valid():
            form.save(commit=True)
            return redirect('profile', user.username)
        else:
            print(form.errors)

    return render(request, 'rango/profile.html', {'userprofile': userprofile, 'selecteduser': user, 'form': form})


@login_required
def list_profiles(request):
    #user_list = User.objects.all()
    userprofile_list = UserProfile.objects.all()
    return render(request, 'rango/list_profiles.html', { 'userprofile_list' : userprofile_list})


def track_url(request):

    page_id = None
    if request.method == 'GET':
        if 'page_id' in request.GET:
            page_id = request.GET['page_id']
    if page_id:
        try:
            page = Page.objects.get(id=page_id)
            page.views = page.views +1
            page.save()
            #return redirect(page.url)
            return HttpResponseRedirect(page.url)
        except:
            return HttpResponse("Page id {0} not found". format(page.id))
    print("No page_id in get string")
    return redirect(reverse('index'))

# Commented because of use django-registration-redux
""""
def user_login(request):

    if request.method == 'POST':
        # Gather the username and password provided by the user.
        # This information is obtained from the login form.
        # We use request.POST.get('<variable>') as opposed
        # to request.POST['<variable>'], because the
        # request.POST.get('<variable>') returns None if the
        # value does not exist, while request.POST['<variable>']
        # will raise a KeyError exception.
        username = request.POST.get('username')
        password = request.POST.get('password')

        # If it is a valid combination, a User object is returned.
        user = authenticate(username=username, password=password)

        # If we have a User object, the details are correct.
        # If None (Python's way of representing the absence of a value), no user
        # with matching credentials was found.
        if user:
            # Is the account active? It could have been disabled.
            if user.is_active:
                # If the account is valid and active, we can log the user in.
                # We'll send the user back to the homepage.
                login(request, user)
                return HttpResponseRedirect(reverse('index'))
            else:
                # An inactive account was used - no logging in!
                return HttpResponse('Your rango account is disabled')
        else:
            # Bad login details were provided. Is not possible log the user in
            print('Invalid login details {0}, {1}'.format(username, password))
            return HttpResponse('Invalid login details supplied.')

    # The request is not a HTTP POST, so display the login form.
    # This scenario would most likely be a HTTP GET.
    else:
        # No context variables to pass, blank dictionary object
        return render(request, 'rango/login.html', {})
"""

 # COMMENTED BECAUSE OF USE DJANGO-REGISTRATION-REDUX
# Use the login_required() decorator to ensure only those logged in can access
# the view.
"""
@login_required
def user_logout(request):
    #Since we know the user is logged in, we can log them out
    logout(request)
    return HttpResponseRedirect(reverse('index'))



# Django's decorator. Python will execute it before executing the code
# of the function/method.
@login_required
def restricted(request):
    return HttpResponse("Since you're logged in, you can see this text!")

"""
























