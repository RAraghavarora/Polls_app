# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render,get_object_or_404
from django.http import Http404

# Create your views here.
from django.http import HttpResponse,HttpResponseRedirect
from .models import Question,Choice
from django.urls import reverse

def index(request):
	latest_question_list=Question.objects.order_by('-pub_date')[:5]
	#template = loader.get_template('polls/index.html')
	context= { 'latest_question_list':latest_question_list}
	#output=', '.join([q.question_text for q in latest_question_list])
	#return HttpResponse(template.render(context, request))
	return render(request, 'polls/index.html',context)
	#return HttpResponse("Hello, world. You're at the polls index")

def detail(request, question_id):
	try:
		question = Question.objects.get(pk=question_id)
	except Question.DoesNotExist:
		raise Http404("Question does not exist")
	# question=get_object_or_404(Question, pk=question_id)
	return render(request, 'polls/detail.html', {'question':question})

def results(request, question_id):
	response= "You're looking at the solutions of the question no. : %s."
	#return HttpResponse(response % question_id)
	question = get_object_or_404(Question, pk=question_id)
	return render(request, 'polls/results.html', {'question':question})

def vote(request, question_id):
	question=get_object_or_404(Question, pk=question_id)
	try:
		selected_choice = question.choice_set.get(pk=request.POST['choice'])
	except (KeyError, Choice.DoesNotExist):
		return render(request, 'polls/detail.html',{'question':question, 'error_message':"You didn't select a choice.",
			})
	else:
		selected_choice.votes+=1
		selected_choice.save()
	return HttpResponseRedirect(reverse('polls:results', args=(question.id,)))

