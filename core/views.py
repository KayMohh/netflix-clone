from django.shortcuts import render, redirect
from django.contrib.auth.models import User, auth
from django.contrib import messages
from django.contrib.auth.decorators import login_required

from .models import Movie

# Create your views here.
@login_required(login_url='login')
def index (request):
      movies = Movie.objects.all() # Fetch all movies from the database

      featured_movie = None # Initialize as None
      if movies.exists(): # Only try to get a featured movie if there are movies
        # Option 1: Get the first movie (simple)
        featured_movie = movies.first()
        # Option 2: Get a random movie (requires more than one movie in DB, can be slower for large DBs)
        # from django.db.models import Count # If you choose this, add this import at the top
        # featured_movie = Movie.objects.annotate(num_movies=Count('id')).order_by('?').first() # A more robust random
        # Option 3: Get a specific movie by a field, e.g., Movie.objects.get(title="Your Featured Movie Title")
        # Be careful with .get() if the object might not exist; use .filter().first() instead.

      context = {
        'movies' : movies, # Pass the QuerySet of all movies
        'featured_movie': featured_movie, # Pass the single featured movie
    }
      return render(request, 'index.html', context)
    
def login(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']

        user = auth.authenticate(username=username, password=password)

        if user is not None:
            auth.login(request, user)
            return redirect('/')
        else:
            messages.info(request, 'Credentials Invalid')
            return redirect('login')
    
    return render(request, 'login.html')

@login_required(login_url='login')
def movie(request, pk):
    movie_uuid = pk
    movie_details = Movie.objects.get(uu_id=movie_uuid)

    context = {
        'movie_details': movie_details
    }

    return render(request, 'movie.html', context)

def signup(request):
    if request.method == 'POST':
        email = request.POST['email']
        username = request.POST['username']
        password = request.POST['password']
        password2 = request.POST['password2']

        if password == password2:
            if User.objects.filter(email=email).exists():
                messages.info(request, 'Email Taken')
                return redirect('signup')
            elif User.objects.filter(username=username).exists():
                messages.info(request, 'Username Taken')
                return redirect('signup')
            else:
                user = User.objects.create_user(username=username, email=email, password=password)
                user.save()

                user_login = auth.authenticate(username=username, password=password)
                auth.login(request, user_login)
                return redirect('/')
        else:
            messages.info(request, 'Password Not Matching')
            return redirect('signup')
    else:
        return render (request, 'signup.html')