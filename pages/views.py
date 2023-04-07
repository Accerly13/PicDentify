from django.shortcuts import render
from django.views.generic import TemplateView
from django.shortcuts import render
from google_images_search import GoogleImagesSearch
# Create your views here.
class HomeView(TemplateView):
    template_name = 'home.html'

    def post(self, request):
        print(request)
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


class Dashboard(TemplateView):
    template_name = 'teacherDashboard.html'

class StudentDashboard(TemplateView):
    template_name = 'studentDashboard.html'