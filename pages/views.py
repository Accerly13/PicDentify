from django.shortcuts import render, redirect, reverse
from django.views.generic import TemplateView
from .models import AdminUser, AdminKey, Topics, Difficulty
from django.contrib import messages
from django.http import HttpResponse, JsonResponse
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout, authenticate, login
from django.core.cache import cache
import random
import string
import requests
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
            username = request.POST['existing_user']
            password = request.POST['password_existing']
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                request.session['username'] = username
                request.session.save()
            return render(request, 'teacherDashboard.html')
            
class Dashboard(LoginRequiredMixin, TemplateView):
    template_name = 'teacherDashboard.html'

    def get(self, request):
        user = AdminUser.objects.get(username=request.session.get('username'))
        def create_topic(topic_name):
            topics = Topics.objects.all()
            try:
                Topics.objects.get(topic_name=topic_name, owner_id=user.admin_id)
            except:
                if topic_name == "Synonyms":
                    topic = Topics.objects.create(topic_id=topics.count()+1, topic_name=topic_name, owner_id=user.admin_id)
                    topic.save()
                    for i in range(1, 4):
                        difficulty = Difficulty.objects.all()
                        if i == 1:
                            word_list = "simple, smooth, quick, ready, soft, clear, cold, hot, small, big"
                            difficulty_save = Difficulty.objects.create(difficulty_id=difficulty.count()+1, difficulty_name='easy',
                                            words=word_list, topic_id=topic.topic_id, time_limit=10,
                                            points_per_question=10)
                            difficulty_save.save()
                        elif i == 2:
                            word_list = "ladder, lady, lamp, land, large, last, late, lately, laugh, lazy"
                            difficulty_save = Difficulty.objects.create(difficulty_id=difficulty.count()+1, difficulty_name='medium',
                                            words=word_list, topic_id=topic.topic_id, time_limit=12,
                                            points_per_question=20)
                            difficulty_save.save()
                        elif i == 3:
                            word_list = "excavate, gallows, mason, sanguine, accord, bereft, blanch, caesura, briar, elegiac"
                            difficulty_save = Difficulty.objects.create(difficulty_id=difficulty.count()+1, difficulty_name='difficult',
                                            words=word_list, topic_id=topic.topic_id, time_limit=15,
                                            points_per_question=30)
                            difficulty_save.save()

                elif topic_name == "Antonyms":
                    topic = Topics.objects.create(topic_id=topics.count()+1, topic_name=topic_name, owner_id=user.admin_id)
                    topic.save()
                    for i in range(1, 4):
                        difficulty = Difficulty.objects.all()
                        if i == 1:
                            word_list = "simple, smooth, quick, ready, soft, clear, cold, hot, small, big"
                            difficulty_save = Difficulty.objects.create(difficulty_id=difficulty.count()+1, difficulty_name='easy',
                                                words=word_list, topic_id=topic.topic_id, time_limit=10,
                                                points_per_question=10)
                            difficulty_save.save()
                        elif i == 2:
                            word_list = "ladder, lady, lamp, land, large, last, late, lately, laugh, lazy"
                            difficulty_save = Difficulty.objects.create(difficulty_id=difficulty.count()+1, difficulty_name='medium',
                                                words=word_list, topic_id=topic.topic_id, time_limit=12,
                                                points_per_question=20)
                            difficulty_save.save()
                        elif i == 3:
                            word_list = "excavate, gallows, mason, sanguine, accord, bereft, blanch, caesura, briar, elegiac"
                            difficulty_save = Difficulty.objects.create(difficulty_id=difficulty.count()+1, difficulty_name='difficult',
                                                words=word_list, topic_id=topic.topic_id, time_limit=15,
                                                points_per_question=30)
                            difficulty_save.save()
                elif topic_name == "Homonyms":
                    topic = Topics.objects.create(topic_id=topics.count()+1, topic_name=topic_name, owner_id=user.admin_id)
                    topic.save()
                    for i in range(1, 4):
                        difficulty = Difficulty.objects.all()
                        if i == 1:
                            word_list = "simple, smooth, quick, ready, soft, clear, cold, hot, small, big"
                            difficulty_save = Difficulty.objects.create(difficulty_id=difficulty.count()+1, difficulty_name='easy',
                                            words=word_list, topic_id=topic.topic_id, time_limit=10,
                                            points_per_question=10)
                            difficulty_save.save()
                        elif i == 2:
                            word_list = "ladder, lady, lamp, land, large, last, late, lately, laugh, lazy"
                            difficulty_save = Difficulty.objects.create(difficulty_id=difficulty.count()+1, difficulty_name='medium',
                                            words=word_list, topic_id=topic.topic_id, time_limit=12,
                                            points_per_question=20)
                            difficulty_save.save()
                        elif i == 3:
                            word_list = "excavate, gallows, mason, sanguine, accord, bereft, blanch, caesura, briar, elegiac"
                            difficulty_save = Difficulty.objects.create(difficulty_id=difficulty.count()+1, difficulty_name='difficult',
                                            words=word_list, topic_id=topic.topic_id, time_limit=15,
                                            points_per_question=30)
                            difficulty_save.save()
                elif topic_name == "Hyponyms":
                    topic = Topics.objects.create(topic_id=topics.count()+1, topic_name=topic_name, owner_id=user.admin_id)
                    topic.save()
                    for i in range(1, 4):
                        difficulty = Difficulty.objects.all()
                        if i == 1:
                            word_list = "simple, smooth, quick, ready, soft, clear, cold, hot, small, big"
                            difficulty_save = Difficulty.objects.create(difficulty_id=difficulty.count()+1, difficulty_name='easy',
                                            words=word_list, topic_id=topic.topic_id, time_limit=10,
                                            points_per_question=10)
                            difficulty_save.save()
                        elif i == 2:
                            word_list = "ladder, lady, lamp, land, large, last, late, lately, laugh, lazy"
                            difficulty_save = Difficulty.objects.create(difficulty_id=difficulty.count()+1, difficulty_name='medium',
                                            words=word_list, topic_id=topic.topic_id, time_limit=12,
                                            points_per_question=20)
                            difficulty_save.save()
                        elif i == 3:
                            word_list = "excavate, gallows, mason, sanguine, accord, bereft, blanch, caesura, briar, elegiac"
                            difficulty_save = Difficulty.objects.create(difficulty_id=difficulty.count()+1, difficulty_name='difficult',
                                            words=word_list, topic_id=topic.topic_id, time_limit=15,
                                            points_per_question=30)
                            difficulty_save.save()
                elif topic_name == "Homographs":
                    topic = Topics.objects.create(topic_id=topics.count()+1, topic_name=topic_name, owner_id=user.admin_id)
                    topic.save()
                    for i in range(1, 4):
                        difficulty = Difficulty.objects.all()
                        if i == 1:
                            word_list = "simple, smooth, quick, ready, soft, clear, cold, hot, small, big"
                            difficulty_save = Difficulty.objects.create(difficulty_id=difficulty.count()+1, difficulty_name='easy',
                                            words=word_list, topic_id=topic.topic_id, time_limit=10,
                                            points_per_question=10)
                            difficulty_save.save()
                        elif i == 2:
                            word_list = "ladder, lady, lamp, land, large, last, late, lately, laugh, lazy"
                            difficulty_save = Difficulty.objects.create(difficulty_id=difficulty.count()+1, difficulty_name='medium',
                                            words=word_list, topic_id=topic.topic_id, time_limit=12,
                                            points_per_question=20)
                            difficulty_save.save()
                        elif i == 3:
                            word_list = "excavate, gallows, mason, sanguine, accord, bereft, blanch, caesura, briar, elegiac"
                            difficulty_save = Difficulty.objects.create(difficulty_id=difficulty.count()+1, difficulty_name='difficult',
                                            words=word_list, topic_id=topic.topic_id, time_limit=15,
                                            points_per_question=30)
                            difficulty_save.save()
            
        create_topics = ["Synonyms", "Antonyms", "Homonyms", "Hyponyms", "Homographs"]
        for topic in create_topics:
            create_topic(topic)
        topics = Topics.objects.filter(owner_id=user.admin_id)
        return render(request, 'teacherDashboard.html', {'user_key':user.user_key, 'topics': topics})
    
    def post(self, request):
        user = AdminUser.objects.get(username=request.session.get('username'))
        difficulty = Difficulty.objects.all()
        word_list = []
        for i in range(1, int(request.POST['num_words']) + 1):
            word_list.append(request.POST['word'+str(i)])
        if '' not in word_list:
            try:
                isTopic = Topics.objects.get(topic_name=request.POST['addTopic'])
                Difficulty.objects.create(difficulty_id=difficulty.count()+1, difficulty_name=request.POST['difficulty'],
                                          words=', '.join(word_list), topic_id=isTopic.topic_id, time_limit=request.POST['time_limit'],
                                          points_per_question=request.POST['points_per_question'])
            except:
                topics = Topics.objects.all()
                topic = Topics.objects.create(topic_id=topics.count()+1, topic_name=request.POST['addTopic'], owner_id=user.admin_id)
                topic.save()
                Difficulty.objects.create(difficulty_id=difficulty.count()+1, difficulty_name=request.POST['difficulty'],
                                          words=', '.join(word_list), topic_id=topic.topic_id, time_limit=request.POST['time_limit'],
                                          points_per_question=request.POST['points_per_question'])

        return render(request, 'teacherDashboard.html')

class StudentDashboard(TemplateView):
    template_name = 'studentDashboard.html'

    def get(self, request):
        try:
            user = AdminUser.objects.get(username=request.session['username'])
            topics = Topics.objects.filter(owner_id=user.admin_id)
            return render(request, 'studentDashboard.html', {'topics':topics})
        except:

            return redirect('/studentlogin/')
        
    def post(self, request):
        if request.POST.get('difficulty') == 'easy':
            try:
                questions = Difficulty.objects.get(difficulty_name='easy', topic_id=request.POST.get('topic_id'))
                return JsonResponse({'questions': questions.difficulty_id})
            except: 
                return redirect('/studentdashboard/')
        elif request.POST.get('difficulty') == 'medium':
            try:
                questions = Difficulty.objects.get(difficulty_name='medium', topic_id=request.POST.get('topic_id'))
                return JsonResponse({'questions': questions.difficulty_id})
            except: 
                return redirect('/studentdashboard/')
        else:
            try:
                questions = Difficulty.objects.get(difficulty_name='difficult', topic_id=request.POST.get('topic_id'))
                return JsonResponse({'questions': questions.difficulty_id})
            except: 
                return redirect('/studentdashboard/')

class StudentActivity(TemplateView):

    def get(self, request):
        def fetch_words():
            response = requests.get('https://random-word-api.herokuapp.com/word')
            if response.status_code == 200:
                word = response.json()[0]
                return word
            else:
                print('Error fetching word')

        def fetch_image(query):
            url = f'https://api.unsplash.com/photos/random/?count=10&query={query}&client_id=tl59FZ7ave-tfL1BOjZMfKxACAF1QFglZyc2O-SMbg8'
            # replace YOUR_ACCESS_KEY with your actual Unsplash API access key
            response = requests.get(url)
            image_urls = []
            if response.status_code == 200:
                data = response.json()
                for image_data in data:
                    image_url = image_data['urls']['regular']
                    image_urls.append(image_url)
                return image_urls
            else:
                image_urls = ["","","","","","","","","",""]
                return image_urls
        
        csrf_token = request.META.get('HTTP_COOKIE', '').split(';')
        questions = Difficulty.objects.get(difficulty_id=csrf_token[0])
        words = questions.words.split(',')

        cleaned_words = [word.strip() for word in words]

        persistent_variable = cache.get('my_persistent_variable')

        # If the persistent variable doesn't exist yet, initialize it
        if persistent_variable is None or persistent_variable == len(words):
            persistent_variable = 0
            cache.set('my_persistent_variable', persistent_variable)

        # Increment the persistent variable
        persistent_variable += 1
        cache.set('my_persistent_variable', persistent_variable)
            
        image_url = fetch_image(cleaned_words[persistent_variable-1])
        choices = []
        for i in range(3):
            choices.append(fetch_words())
        choices.append(cleaned_words[persistent_variable-1])
        random.shuffle(choices)
        random_number = random.randint(0, 9)
        return render(request, 'studentActivity.html', {'questions':questions, 'words': cleaned_words[persistent_variable-1], 'start_index':persistent_variable, 'img_url':image_url[random_number], 'length':len(words), 'choices':choices})
    def post(self, request):
        if request.POST.get('choice'):
            csrf_token = request.META.get('HTTP_COOKIE', '').split(';')
            questions = Difficulty.objects.get(difficulty_id=csrf_token[0])
            words = questions.words.split(',')

            cleaned_words = [word.strip() for word in words]

            if request.POST.get('choice') not in cleaned_words:
                return JsonResponse({'answerVerify': False})
            else:
                return JsonResponse({'answerVerify': True})





       
class StudentLogin(TemplateView):
    template_name = 'studentLogin.html'

    def post(self, request):
        if request.POST.get('admin_key'):
            try:
                admin_user = AdminUser.objects.get(user_key=request.POST['admin_key'])
                username = admin_user.username
                password = admin_user.password
                user = authenticate(request, username=username, password=password)
                if user is not None:
                    login(request, user)
                    request.session['username'] = username
                    request.session.save()
                return JsonResponse({'adminKeyVerify': True})
            except:
                return JsonResponse({'adminKeyVerify': False})