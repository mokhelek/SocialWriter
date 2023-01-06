from django.shortcuts import render


from django.shortcuts import render, redirect
from django.contrib.auth import login
from django.contrib.auth.forms import UserCreationForm

from django.contrib.auth.models import User 

from .models import Profile
from .forms import SignUpForm

# Create your views here.
def register(request):
 
    if request.method != 'POST':
        # Display blank registration form. 
        form = SignUpForm()
    else:
        # Process completed form.
        form = SignUpForm(data=request.POST)
        
        if form.is_valid():
            new_user = form.save()
            get_id = form.instance.id  # get the id of a use--it has a username inside
            users = User.objects.get(id=get_id) # get the new user
            profiles = Profile.objects.create( name = users)
            profiles.save()

            new_user.save()
            
            #profiles.name = new_user.username  # please note
            #profiles.save(update_fields=['name'])
            # Log the user in and then redirect to home page.
            login(request, new_user)
            return redirect('blogyapp:home1')
    context = {'form': form}
    return render(request, 'registration/register.html', context)

def logout_page(request):
    return render(request, 'registration/logged_out.html')

