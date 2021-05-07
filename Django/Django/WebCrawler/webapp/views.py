from django.shortcuts import render

from django.http import HttpResponse, request
from django.core import serializers
from django.template import Context
from .Search import Search
from .GetURLS import GetURLS


def home(request):
	return render(request, 'index.html')
	
def adminhomedef(request):
	if "adminid" in request.session:
		uid=request.session["adminid"]
		return render(request, 'admin_home.html')

	else:
		return render(request, 'admin.html')

	

def adminlogoutdef(request):
	try:
		del request.session['adminid']
	except:
		pass
	return render(request, 'admin.html')	
	
def adminlogindef(request):
	return render(request, 'admin.html')

def adminloginactiondef(request):
	if request.method=='POST':
		uid=request.POST['uid']
		pwd=request.POST['pwd']
		
		if uid=='admin' and pwd=='admin':
			request.session['adminid']='admin'
			return render(request, 'admin_home.html')

		else:
			return render(request, 'admin.html',{'msg':"Login Fail"})

	else:
		return render(request, 'admin.html')

def topicsearch(request):
	return render(request, 'asearch.html')

def searchurls(request):
	keys=request.POST['keys']
	request.session['keys']=keys
	import time
	s = time.clock()
	data=Search.main(keys)
	e = time.clock()

	t = round(e - s, 5)


	
	return render(request, 'results.html',{'data':data,'t':t})

def extracturls(request):
	uid=request.POST['uid']
	print('--------------->',uid)
	import webbrowser
	webbrowser.open(uid)



	d=GetURLS.process(uid)
	
	request.session['uid']=uid

	return render(request, 'eresults.html',{'data':d})

def download(request):
	file=request.POST['text']
	
	import json
	url=request.session['uid']
	
	
	d={}
	d['URL']=url
	d['Webcontent']=file
	import random

	R=random.randint(0,90000)
	R=str(R)+".json"
	out_file = open('Json'+"/"+R, "w")
	json.dump(d, out_file, indent = 1)
	out_file.close()


	return render(request, 'succ.html',{'data':R})

