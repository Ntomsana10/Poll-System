from typing import Any
from django.db.models.query import QuerySet
from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse, HttpResponseRedirect
from django.http import Http404
from django.urls import reverse
from django.views import generic
from .models import Question, Choice
from django.utils import timezone

# Create your views here.
# @DjangoAdmin10

class IndexView(generic.ListView):
    """
    Return the last five published questions (not including those set to be
    published in the future).
    """
    template_name = "polls/index.html/"
    context_object_name = "latest_question_list"

    def get_queryset(self):
        return Question.objects.filter(pub_date__lte=timezone.now()).order_by("-pub_date")[:5]

class DetailView(generic.DetailView):
    model = Question
    template_name = "polls/detail.html"

class ResultsView(generic.DetailView):
    model = Question
    template_name = "polls/results.html "

def vote(request, question_id):
    question = get_object_or_404(Question, pk=question_id)

    try:
        selected_chioce = question.choice_set.get(pk=request.POST['choice'])

    except (KeyError, Choice.DoesNotExist):
        return render(request,
                      "polls/detail.html/",
        {
            "question": question,
            "error message":"You didn't select a choice"
        },)
    
    else:
        selected_chioce.votes += 1
        selected_chioce.save()
        return HttpResponseRedirect(reverse("polls:results", args=(question.id,)))