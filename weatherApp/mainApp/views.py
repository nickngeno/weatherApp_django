import requests
from django.http import Http404
from django.shortcuts import render, redirect, get_object_or_404
from .models import City
from .forms import Cityform


# Create your views here.
def home(request):
    url = 'http://api.openweathermap.org/data/2.5/weather?q={}&units=metric&APPID=2712c0400567a5e1d7a7b69197b35404'
    # city= 'kampala'

    form = Cityform()

    err_msg = ''
    message = ''
    message_class = ''
    if request.method == 'POST':
        form = Cityform(request.POST)
        if form.is_valid():
            name = form.cleaned_data['name']
            # print(name)
            new_city = City.objects.filter(name=name).count()
            if new_city == 0:
                r = requests.get(url.format(name)).json()
                print(r)
                if r['cod'] == 200:
                    form.save()

                else:
                    err_msg = 'City does not exist'

            else:
                err_msg = "there is an existing city in the list!"

        if err_msg:
            message = err_msg
            message_class = 'alert-danger'
        else:
            message = 'city added successfully'
            message_class = 'alert-success'

    cities = City.objects.all()
    weather_data = []
    for city in cities:
        r = requests.get(url.format(city)).json()
        city_weather = {
            'city': city.name,
            'temperature': r['main']['temp'],
            'description': r['weather'][0]['description'],
            'icon': r['weather'][0]['icon'],
        }
        weather_data.append(city_weather)
        print(weather_data)

    context = {
        'weather_data': weather_data,
        'form': form,
        'message': message,
        'message_class': message_class
    }

    return render(request, 'mainApp/home.html', context)


# delete city
def delete_city(request, city_name):
    try:
        City.objects.get(name=city_name).delete()

        return redirect('home')
    except:
        raise Http404("City does not exist!")
