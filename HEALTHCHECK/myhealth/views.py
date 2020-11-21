from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.views.generic import CreateView, UpdateView
from .models import HealthModel
from .forms import HealthForm
from django.urls import reverse_lazy
from .scraping import scrape
import datetime
from .functions import DecisionTreeClass
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required

def listfunc(request):

    object_list = HealthModel.objects.all()

    return render(request, 'list.html', {'object_list' : object_list})



class ScrapeCreate(CreateView):
    template_name = 'create.html'
    model = HealthModel
    form_class = HealthForm
    success_url = reverse_lazy('list')

    def get_initial(self):
        url = 'https://tenki.jp/forecast/2/10/3610/7308/'
        max_temp, weather = scrape(url)
        dt_now = datetime.datetime.now().strftime('%Y-%m-%d')

        return {'max_temp': max_temp, 'weather': weather, 'input_date': dt_now}

class DiaryUpdate(UpdateView):
    template_name = 'update.html'
    model = HealthModel
    form_class = HealthForm

    success_url = reverse_lazy('list')

def analysis(request):
    #get data from DB
    object_list = HealthModel.objects.all()
    max_temp_list = [data.max_temp for data in object_list]
    weather_list = [data.weather for data in object_list]
    condition_list = [data.condition for data in object_list]

    #make model
    dtc_class = DecisionTreeClass()
    dtc_class.fit(max_temp_list, weather_list, condition_list)

    #predict conditon
    url = 'https://tenki.jp/forecast/2/10/3610/7308/'
    max_temp, weather = scrape(url)
    predicted_condition = dtc_class.predict(max_temp, weather)

    if predicted_condition == 0:
        result = '大丈夫です'
    elif predicted_condition == 1:
        result = '少し気をつけましょう'
    else:
        result = '気をつけましょう'


    most_feature = dtc_class.featureimportance()

    if most_feature == '最高気温':
        recomend = '暑い日は家にいましょう'
    else:
        recomend = '天気が悪い日は家にいましょう'

    return render(request, 'analysis.html',{'result': result, 'most_feature': most_feature, 'recomend': recomend})


def signupfunc(request):
    if request.method == 'POST':
        input_username= request.POST['username']
        input_password = request.POST['password']
        try:
            User.objects.get(username=input_username)
            return render(request, 'signup.html', {'error':'このユーザは登録されています'})

        except:
            user = User.objects.create_user(input_username,'', input_password)
            return render(request, 'signup.html', {'some': 100})

    return render(request, 'signup.html', {'some': 100})

def loginfunc(request):
    if request.method == 'POST':
        input_username= request.POST['username']
        input_password = request.POST['password']
        user = authenticate(request, username=input_username, password=input_password)
        if user is not None:
            login(request, user)
            return redirect('list')

        else:
            return redirect('login')

    return render(request, 'login.html')

def logoutfunc(request):
    logout(request)
    return redirect('login')


def graph(request):

    object_list = HealthModel.objects.all()
    max_temp_list = [data.max_temp for data in object_list]
    condition_list = [data.condition for data in object_list]
    input_date_list = [data.input_date.strftime('%m/%d') for data in object_list]
    input_date_list2 = [data.input_date.day for data in object_list]

    context = {
        'max_temp_list': max_temp_list,
        'condition_list': condition_list,
        'input_date_list': input_date_list,
    }

    return render(request, 'graph.html', context)