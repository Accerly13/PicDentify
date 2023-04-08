from django.shortcuts import render
from django.views.generic import TemplateView
from .models import AdminUser, AdminKey
from django.http import HttpResponse, JsonResponse
from django.shortcuts import render
import random
import string
from google_images_search import GoogleImagesSearch
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
        try:
            AdminKey.objects.get(pk=1)
        except:
            AdminKey.objects.create(key_id=1, admin_key="deped143")
        
        admins = AdminUser.objects.all()
        return render(request, 'loginPage.html', {'admins': admins})
    
    def post(self, request):
        def generate_random_string():
            characters = string.ascii_letters + string.digits
            return ''.join(random.choice(characters) for i in range(8))

        if request.POST.get('admin_key'):
            admin_key_input = request.POST['admin_key']
            check_admin_key = AdminKey.objects.get(pk=1)

            if admin_key_input == check_admin_key.admin_key:
                return JsonResponse({'adminKeyVerify': True})

            else:
               return JsonResponse({'adminKeyVerify': False})
        return JsonResponse({'adminKeyVerify': False})

class Dashboard(TemplateView):
    template_name = 'teacherDashboard.html'

class StudentDashboard(TemplateView):
    template_name = 'studentDashboard.html'