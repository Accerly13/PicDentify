from django.shortcuts import render, redirect
from django.views.generic import TemplateView
from .models import AdminUser, AdminKey
from django.contrib import messages
from django.http import HttpResponse, JsonResponse
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout, authenticate, login
import random
import string
from google_images_search import GoogleImagesSearch

@login_required
def protected_view(request):
    # Your protected view logic here
    return render(request, 'loginPage.html')

def logout_view(request):
    logout(request)
    return redirect('/')
# Create your views here.
class TryView(TemplateView):
    template_name = 'try.html'
    def post(self, request):
        if request.POST.get('search_term'):
            # Get the search term from the POST request
            search_term = request.POST.get('search_term', '')
            
            search_params = {
                'q': search_term,
                'num': 3,
            }
           
            # Initialize the GoogleImagesSearch object
            gis = GoogleImagesSearch('AIzaSyBGL45ZwjasJjRVWH_JmAtYflGArjmNfqE', '5793900b712be4274')         
            # Set the search parameters
            gis.search(search_params)
            # Get the first 10 images from the search results
            results = gis.results()[:10]
            
            # Render the template with the search results
            return render(request, 'home.html', {'results': results})
        
        # Render the search form if the request method is not POST
        return render(request, 'home.html')
class LoginPage(TemplateView):
    template_name = 'loginPage.html'
    def get(self, request):
        print(request.session.get('username'))
        try:
            AdminKey.objects.get(pk=1)
        except:
            AdminKey.objects.create(key_id=1, admin_key="deped143")
        
        admins = AdminUser.objects.all()
        return render(request, 'loginPage.html', {'admins': admins})
    
    def post(self, request):
        def generate_random_string():
            characters = string.ascii_letters + string.digits
            teacher_key = ''.join(random.choice(characters) for i in range(8))
            try:
                if AdminUser.objects.get(user_key=teacher_key):
                    generate_random_string()
            except:
                return teacher_key

        if request.POST.get('admin_key'):
            admin_key_input = request.POST['admin_key']
            check_admin_key = AdminKey.objects.get(pk=1)

            if admin_key_input == check_admin_key.admin_key:
                return JsonResponse({'adminKeyVerify': True})

            else:
               return JsonResponse({'adminKeyVerify': False})
        elif request.POST.get('new_user_hidden'):
            teacher_key = generate_random_string()

            if request.POST['password'] == request.POST['password1']:
                admins = AdminUser.objects.all()

                admin_user = AdminUser.objects.create_superuser(admin_id=admins.count()+1, username=request.POST['new_user'], 
                                                   password=request.POST['password'], user_key=teacher_key)
                admin_user.save()
            else:
                messages.success(request, ("Password didn't match!"))	
                return redirect('/')	
        else:
            username = request.POST['new_user']
            password = request.POST['password']
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
            return render(request, 'teacherDashboard.html')
            
class Dashboard(LoginRequiredMixin, TemplateView):
    template_name = 'teacherDashboard.html'

    def get(self, request):
        print(request.session.get('username'))
        return render(request, 'teacherDashboard.html')

class StudentDashboard(TemplateView):
    template_name = 'studentDashboard.html'

class StudentActivity(TemplateView):
    template_name = 'studentActivity.html'