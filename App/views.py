from datetime import datetime
from django.shortcuts import render
from .models import AuditEntry
from django.contrib.auth.models import User
from django.db.models import Q
import datetime
# Create your views here.
def home(request):
    users = User.objects.all()
    return render(request,'App/home.html',{'users':users})

def last(request):
    Id = request.GET['id']
    DatePrev31Day = datetime.datetime.now()-datetime.timedelta(days=31)
    day,month,year = str(DatePrev31Day.day),str(DatePrev31Day.month),str(DatePrev31Day.year)
    if len(day) == 1:
        day = "0"+day
    if len(month) == 1:
        month = "0"+month
    date = year+"-"+month+"-"+day
    AuditEntry.objects.filter(date__lte=date).delete()
    user = User.objects.filter(id = Id)[0]
    username = user.username

    userLast30daysData = AuditEntry.objects.filter(username__iexact=username)
    # for i in userLast30daysData:
    #     print(i.action, i.date, i.time, i.ip, i.username)
    userLoggedIn = AuditEntry.objects.filter(Q(username__iexact=username) & Q(action__iexact="user_logged_in")).count()
    userLoggedOut = AuditEntry.objects.filter(Q(username__iexact=username) & Q(action__iexact="user_logged_out")).count()
    # print("user Logged in count:",userLoggedIn)
    # print("user Logged out count:",userLoggedOut)
    return render(request,'App/show.html', {'userData':userLast30daysData, 'userLoggedIn':userLoggedIn, 'userLoggedOut':userLoggedOut})

def yesterday(request):
    Id = request.GET['id']
    user = User.objects.filter(id = Id)[0]
    username = user.username
    Yesterday = datetime.datetime.now()-datetime.timedelta(days=1)
    day,month,year = str(Yesterday.day),str(Yesterday.month),str(Yesterday.year)
    if len(day) == 1:
        day = "0"+day
    if len(month) == 1:
        month = "0"+month
    date = year+"-"+month+"-"+day

    userYesterdayData = AuditEntry.objects.filter(Q(username__iexact=username) & Q(date__iexact=date))
    # for i in userYesterdayData:
    #     print(i.action, i.date, i.time, i.ip, i.username)
    userLoggedIn = AuditEntry.objects.filter(Q(username__iexact=username) & Q(date__iexact=date) & Q(action__iexact="user_logged_in")).count()
    userLoggedOut = AuditEntry.objects.filter(Q(username__iexact=username) & Q(date__iexact=date) & Q(action__iexact="user_logged_out")).count()
    # print("user Logged in count:",userLoggedIn)
    # print("user Logged out count:",userLoggedOut)
    return render(request,'App/show.html', {'userData':userYesterdayData, 'userLoggedIn':userLoggedIn, 'userLoggedOut':userLoggedOut})

def today(request):
    Id = request.GET['id']
    user = User.objects.filter(id = Id)[0]
    username = user.username
    currentDT = datetime.datetime.now()
    day,month,year = str(currentDT.day),str(currentDT.month),str(currentDT.year)
    if len(day) == 1:
        day = "0"+day
    if len(month) == 1:
        month = "0"+month
    date = year+"-"+month+"-"+day

    userTodayData = AuditEntry.objects.filter(Q(username__iexact=username) & Q(date__iexact=date))
    # for i in userTodayData:
    #     print(i.action, i.date, i.time, i.ip, i.username)
    userLoggedIn = AuditEntry.objects.filter(Q(username__iexact=username) & Q(date__iexact=date) & Q(action__iexact="user_logged_in")).count()
    userLoggedOut = AuditEntry.objects.filter(Q(username__iexact=username) & Q(date__iexact=date) & Q(action__iexact="user_logged_out")).count()
    # print("user Logged in count:",userLoggedIn)
    # print("user Logged out count:",userLoggedOut)
    return render(request,'App/show.html', {'userData':userTodayData, 'userLoggedIn':userLoggedIn, 'userLoggedOut':userLoggedOut})