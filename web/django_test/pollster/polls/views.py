from django.shortcuts import render
from .models import Question,Choice

# Create your views here.

#Get questions and display them
def index(request):
    latest_question_list=Question.objects.order_by('-pub_date')[:5] #The - in front of pub_date makes it descending
    context={'latest_question_list':latest_question_list}
    return render(request,'polls/index.html',context)

#Show specific Question & Choices
def detail(request,question_id):
    try:
        question=Question.objects.get(pk=question_id)
    except Question.DoesNotExist:
        raise Http404("Question does not exist")
    return render(request,'polls/results.html',{'question':question})

#Get Question & Display Results
def results(request,question_id):
    question=get_object_or_404(Question, pk=question_id)
    return render(request, 'polls/results.html', {'question': question})


