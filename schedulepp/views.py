from django.http import HttpResponse, HttpResponseRedirect, HttpResponseForbidden
from django.template import RequestContext, loader
from django.shortcuts import render, get_object_or_404
from django.core.urlresolvers import reverse

from schedulepp.models import *
from django.utils import simplejson
from schedulepp.helpers import *
from django.contrib.auth import logout
from django.core.urlresolvers import reverse
from django.contrib import messages
import facebook

def index(request):
  print "I'm in Index"
  return render(request, 'schedulepp/MainPage/fbbutton.html', {})

def fb_auth(request):
  print request.POST["auth_tok"]
  request.session["auth_tok"] = request.POST["auth_tok"]
  if (request.session["auth_tok"]): #There is an auth token
    if (is_user(request.session["auth_tok"])):
      id_num = (facebook.GraphAPI(request.session["auth_tok"]).get_object("me"))["id"]
      if (Student.objects.get(fb_id=id_num).schedule == ""):
        return render(request, 'schedulepp/SIOpage/loginpage.html', {})
      return render(request, 'schedulepp/MainPage/main.html', {})
    else:
      if (create_user(request.session["auth_tok"])):
        return render(request, 'schedulepp/SIOpage/loginpage.html', {})
  return render(request,'schedulepp/schedulepp.html', {})

def sio_request(request):
  if (request.session["auth_tok"] and request.POST["andrew"] and request.POST["passwd"]):
    update_sio(request.session["auth_tok"], request.POST["andrew"], request.POST["passwd"])
    return render(request, 'schedulepp/MainPage/main.html', {})
  return render(request, 'schedulepp/fbbutton.html', {})
