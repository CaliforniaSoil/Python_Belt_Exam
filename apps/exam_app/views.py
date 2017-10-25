from django.shortcuts import render, redirect
from .models import *
from django.contrib import messages

def index(request):
	return render(request, 'exam_app/index.html')

def current_user(request):
	return User.objects.get(id = request.session['id'])

def register(request):
   
    postData = {
        'name' : request.POST['name'],
        'alias' : request.POST['alias'],
        'email' : request.POST['email'],
        'password' : request.POST['password'],
        'confirm' : request.POST['confirm'],
    }
 
    errors = User.objects.register(postData)
    if len(errors) == 0:

        request.session['id'] = User.objects.filter(email=postData['email'])[0].id
        request.session['name'] = postData['name']
        return redirect('/quotes')
    else:
        for errors in errors:
            messages.info(request, errors)
        return redirect('/')

def login(request):
    postData = {
        'email' : request.POST['email'],
        'password' : request.POST['password']
    }
    errors = User.objects.login(postData)
    if len(errors) == 0:
        request.session['id'] = User.objects.filter(email=postData['email'])[0].id
        request.session['name'] = User.objects.filter(email=postData['email'])[0].name
        return redirect('/quotes')
    for error in errors:
        messages.info(request, errors)
    return redirect('/')


def user(request, id):

	user =  User.objects.get(id = id)
	context = {
		'user': user,
		'favorites': user.favorites.all()		
	}
	return render(request, 'exam_app/user.html', context)

def quotes(request):
	user = current_user(request)

	context = {
		'user': user,
		'quotable_quotes': Quote.objects.exclude(favorites = user),
		'favorites': user.favorites.all()
	}

	return render(request, 'exam_app/dashboard.html', context)


def create(request):
	if request.method != 'POST':
		return redirect('/')
	
	check = Quote.objects.validateQuote(request.POST)
	if request.method != 'POST':
		return redirect('/quotes')
	if check[0] == False:
		for error in check[1]:
			messages.add_message(request, messages.INFO, error, extra_tags="add_item")
			return redirect('/quotes')
	if check[0] == True:

		quote = Quote.objects.create(
			content = request.POST.get('content'),
			poster = current_user(request),
			author = request.POST.get('author')
			)

		return redirect('/quotes')
	return redirect('/quotes')

def addfav(request, id):

	user = current_user(request)
	favorite = Quote.objects.get(id=id)

	user.favorites.add(favorite)

	return redirect('/quotes')

def removefav(request, id):

	user = current_user(request)
	favorite = Quote.objects.get(id=id)

	user.favorites.remove(favorite)

	return redirect('/quotes')

def logout(request):
		request.session.clear()
		return redirect('/')

