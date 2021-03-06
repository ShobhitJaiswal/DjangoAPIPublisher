# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.contrib import messages
from django.http import JsonResponse, HttpResponseRedirect
from django.shortcuts import render, HttpResponse, redirect
from django.views.decorators.csrf import csrf_exempt, csrf_protect
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import user_passes_test
from models import Publisher, API
from models import UserToken as User
import bcrypt, json, requests

# Create your views here.

@csrf_exempt
def index(request):
    try:
        if request.session['id'] is None:
            return render(request, 'register/login.html')
        else:
            return redirect('/admin')
    except Exception as e:
        return render(request, 'register/login.html')


@csrf_exempt
def register(request):
    errors = User.objects.validator(request.POST)
    if len(errors):
        for tag, error in errors.iteritems():
            messages.error(request, error, extra_tags=tag)
        return redirect('/')

    hashed_password = bcrypt.hashpw(request.POST['password'].encode(), bcrypt.gensalt())
    user = User.objects.create(first_name=request.POST['first_name'], last_name=request.POST['last_name'], password=hashed_password, email=request.POST['email'])
    user.save()
    request.session['id'] = user.id
    return redirect('/admin')

@csrf_exempt
def userlogin(request):
    if (User.objects.filter(username=request.POST['login_username']).exists()):
        user=User.objects.filter(username=request.POST['login_username'])[0]
        if user.token is None:
            payload={"partnerid":"ott615"}
            url="http://newott.planetcast.in:6098/gettoken"
            token=requests.post(url,data=payload).json()["Token"].encode('utf-8')
            user.token = token
            user.save()
        users = authenticate(request,username=user.username, password=request.POST['login_password'])
        if users is not None:
            login(request,users)
            request.session['id'] = user.id
            if user.is_superuser == True:           
                return redirect('/admin')
            else:
                return redirect("/home")
	else:
		return redirect("/")
    return redirect('/')

def userlogout(request):
    url="http://newott.planetcast.in:6098/logout"
    payload={"partnerid":"ott615"}
    headers={"token":str(request.user.token)}
    remove_token=requests.post(url,headers=headers,data=payload)
    if request.session["id"] is not None:
        token=User.objects.get(id=request.user.id)
        token.token = None
        token.save()
        del request.session["id"]
        logout(request)
        return HttpResponseRedirect("/")

@login_required(login_url='/')
@user_passes_test(lambda u: u.is_superuser)
def success(request):
    user = User.objects.get(id=request.session['id'])
    userall=User.objects.filter(is_superuser=False)
    publisher=Publisher.objects.all()
    api=API.objects.all()

    context = {
        "user": user,
        "userall": userall,
        "publisher":publisher,
        "api":api
    }
    return render(request, 'register/success.html', context)

@csrf_exempt
def dev(request):
    user = User.objects.get(id=request.session['id'])
    userall=User.objects.all()
    publisher=Publisher.objects.all()
    api=API.objects.all()

    context = {
        "user": user,
        "userall": userall,
        "publisher":publisher,
        "api":api
    }
    return render(request, 'register/dev.html', context)

@csrf_exempt
def insert(request):
    try:
        hashed_password = bcrypt.hashpw(request.POST['password'].encode(), bcrypt.gensalt())
        payload={"partnerid":"ott615"}
        url="http://newott.planetcast.in:6098/gettoken"
        token=requests.post(url,data=payload).json()["Token"].encode('utf-8')
        user = User.objects.create_user(request.POST['first_name']+'_'+request.POST['last_name'],request.POST['email'],request.POST['password'])
        user.token=token
        user.first_name=request.POST['first_name']
        user.last_name=request.POST['last_name']
        user.save()
        users_data={"id":user.id,"error":False,"Message":"User Added Successfully"}
        return JsonResponse(users_data,safe=False)
    except:
        users_data={"error":True,"Message":"Failed to Add User"}
        return JsonResponse(users_data,safe=False)

@csrf_exempt
def update(request):
    data=request.POST.get("data")
    post_data=json.loads(data)
    try:
        for i in post_data:
            users_obj=User.objects.get(id=i['id'])
            users_obj.first_name=i['first_name']
            users_obj.last_name=i['last_name']
            users_obj.email=i['email']
            users_obj.save()
        user_data={"error":False,"errorMessage":"Updated Successfully"}
        return JsonResponse(user_data,safe=False)
    except:
        user_data={"error":True,"errorMessage":"Failed to Update Data"}
        return JsonResponse(user_data,safe=False)

@csrf_exempt
def delete(request):
    id=request.POST.get("id")
    tag=str(request.POST.get("tag"))
    if tag=="users":
        obj=User.objects.get(id=id)
    elif tag=="publisher":
        obj=Publisher.objects.get(id=id)
    elif tag=="api":
        obj=API.objects.get(name_id=id)

    try:
        obj.delete()
        user_data={"error":False,"errorMessage":"Deleted Successfully"}
        return JsonResponse(user_data,safe=False)
    except:
        user_data={"error":True,"errorMessage":"Failed to Delete User"}
        return JsonResponse(user_data,safe=False)

@csrf_exempt
def insertpublisher(request):
    errors = Publisher.objects.validator(request.POST)
    if len(errors):
        for tag, error in errors.iteritems():
            messages.error(request, error, extra_tags=tag)
        return redirect('/')
    try:
        publisher = Publisher.objects.create(name=request.POST['pname'], url=request.POST['url'])
        publisher.save()
        users_data={"id":publisher.id,"error":False,"Message":"Publisher Added Successfully"}
        return JsonResponse(users_data,safe=False)
    except Exception as e:
        users_data={"error":True,"Message":"Failed to Add Publisher"}
        return JsonResponse(users_data,safe=False)

@csrf_exempt
def updatepublisher(request):
    data=request.POST.get("data")
    post_data=json.loads(data)
    try:
        for i in post_data:
            pub_obj=Publisher.objects.get(id=i['id'])
            pub_obj.name=i['p_name']
            pub_obj.url=i['url']
            pub_obj.save()
        pub_data={"error":False,"errorMessage":"Updated Successfully"}
        return JsonResponse(pub_data,safe=False)
    except:
        pub_data={"error":True,"errorMessage":"Failed to Update Data"}
        return JsonResponse(pub_data,safe=False)

@csrf_exempt
def insertapi(request):
    param=request.POST.getlist('param[]')
    params={}
    for i in range(0,len(param),2):
        key=param[i]
        for j in range(i+1,len(param)):
            value=param[j]
            break
        params[key]=value
    errors = API.objects.validator(request.POST)
    if len(errors):
        for tag, error in errors.iteritems():
            messages.error(request, error, extra_tags=tag)
        return redirect('/')
    try:
        pubname=Publisher.objects.filter(name=request.POST['pub'])
        for i in pubname:
            name=i.name
            api = API(name_id=i.id,api=request.POST['apis'],api_parameters=params)
            api.save()
            users_data={"id":api.id,"error":False,"Message":"API Added Successfully for "+request.POST['pub']}
            return JsonResponse(users_data,safe=False)
    except Exception as e:
        users_data={"error":True,"Message":"Failed to Add API"}
        return JsonResponse(users_data,safe=False)

@csrf_exempt
def updateapi(request):
    data=request.POST.get("data")
    post_data=json.loads(data)
    try:
        for i in post_data:
            api_obj=API.objects.get(name_id=i['id'])
            api_obj.api=i['api_name']
            api_obj.save()
        pub_data={"error":False,"errorMessage":"Updated Successfully"}
        return JsonResponse(pub_data,safe=False)
    except Exception as e:
        pub_data={"error":True,"errorMessage":"Failed to Update Data"}
        return JsonResponse(pub_data,safe=False)

@csrf_exempt
def deleteapi(request):
    id=request.POST.get("id")
    try:
        obj=API.objects.get(id=id)
        obj.delete()
        user_data={"error":False,"errorMessage":"Deleted Successfully"}
        return JsonResponse(user_data,safe=False)
    except Exception as e:
        user_data={"error":True,"errorMessage":"Failed to Delete User"}
        return JsonResponse(user_data,safe=False)

@csrf_exempt
@login_required(login_url='/')
def home(request):    
    try:
        tag=str(request.POST.get("tag"))
    except:
        tag=""
    if tag == "None":
        publisher=Publisher.objects.all()
        context = {
            "publisher":publisher,
        }
        return render(request, 'register/home.html',context)
    elif tag == "response":
        publish=str(request.POST.get("publisher"))
        uri=str(request.POST.get("uri"))
        try:
            id=request.session['id']
            user=User.objects.get(id=id)
            token=user.token
            publisher=Publisher.objects.filter(name=publish) 
            for i in publisher:
                api=API.objects.filter(api=uri)
                for j in api:
                    headers={"token":token}
                    # headers={}
                    url=i.url+uri
                    x=requests.post(url,headers=headers,data=eval(j.api_parameters))
                    data={
                        "result":x.json(),
                        "elapsed":x.elapsed.total_seconds(),
                        "status":x.status_code,
                    }
                    return JsonResponse(data,safe=False)
        except Exception as e:
            data={"result":str(e)}
            return JsonResponse(data,safe=False)
    else:
        context=[]
        publisher=Publisher.objects.filter(name=tag) 
        for i in publisher:
            api=list(API.objects.filter(name_id=i.id))
            for j in api:
                context.append(j.api)
            data={
                "api":context,
                "tag":tag,
            }
        return JsonResponse(data,safe=False)