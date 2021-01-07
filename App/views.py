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

def HourMinuteCalculator(data):
    l=[]
    for i in data:
        if i.action == "user_logged_in":
            LoginDate = i.date
            LoginTime = i.time
            l.append(["login",LoginDate,LoginTime])
        elif i.action == "user_logged_out":
            LogoutDate = i.date
            LogoutTime = i.time
            l.append(["logout",LogoutDate,LogoutTime])
        if l[0][0] == "logout":
            del l[0]
    
    if len(l) % 2 != 0:
        l.pop()
    
    m = []
    for j in l:
        YEAR = j[1].year
        MONTH = j[1].month
        DAY = j[1].day
        HOUR = j[2].hour
        MINUTE = j[2].minute
        SECOND = j[2].second
        m.append([YEAR,MONTH,DAY,HOUR,MINUTE,SECOND])
    
    HM = []
    for jk in range(0,len(m),2): 
        TL = m[jk]+m[jk+1]
        b = datetime.datetime(TL[0], TL[1], TL[2], TL[3], TL[4], TL[5]) #login
        a = datetime.datetime(TL[6], TL[7], TL[8], TL[9], TL[10], TL[11]) #logout
        H = a-b
        M = H.total_seconds() / 60 # minute
        H = M / 60  #hour
        d1 = str(TL[2])+"-"+str(TL[1])+"-"+str(TL[0])
        T1 = str(TL[3])+":"+str(TL[4])+":"+str(TL[5])
        d2 = str(TL[8])+"-"+str(TL[7])+"-"+str(TL[6])
        T2 = str(TL[9])+":"+str(TL[10])+":"+str(TL[11])
        dateTime = d1,T1,"To",d2,T2
        HM.append([dateTime,H,M])
    return HM

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
    
    tup = HourMinuteCalculator(userLast30daysData)

    userLoggedIn = AuditEntry.objects.filter(Q(username__iexact=username) & Q(action__iexact="user_logged_in")).count()
    userLoggedOut = AuditEntry.objects.filter(Q(username__iexact=username) & Q(action__iexact="user_logged_out")).count()
    
    return render(request,'App/show.html', {'userData':userLast30daysData, 'userLoggedIn':userLoggedIn, 'userLoggedOut':userLoggedOut, 'tup':tup})

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
    
    tup = HourMinuteCalculator(userYesterdayData)
    
    userLoggedIn = AuditEntry.objects.filter(Q(username__iexact=username) & Q(date__iexact=date) & Q(action__iexact="user_logged_in")).count()
    userLoggedOut = AuditEntry.objects.filter(Q(username__iexact=username) & Q(date__iexact=date) & Q(action__iexact="user_logged_out")).count()
    return render(request,'App/show.html', {'userData':userYesterdayData, 'userLoggedIn':userLoggedIn, 'userLoggedOut':userLoggedOut, 'tup':tup})

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

    tup = HourMinuteCalculator(userTodayData)

    userLoggedIn = AuditEntry.objects.filter(Q(username__iexact=username) & Q(date__iexact=date) & Q(action__iexact="user_logged_in")).count()
    userLoggedOut = AuditEntry.objects.filter(Q(username__iexact=username) & Q(date__iexact=date) & Q(action__iexact="user_logged_out")).count()
    return render(request,'App/show.html', {'userData':userTodayData, 'userLoggedIn':userLoggedIn, 'userLoggedOut':userLoggedOut, 'tup':tup})