from django.shortcuts import render, get_object_or_404
from django.http import HttpResponseRedirect
from django.urls import reverse 
from django.views import generic
from django.utils import timezone

from .models import Choice, Question

class IndexView(generic.ListView):
	template_name = 'polls/index.html'

	context_object_name = 'latest_question_list'

	def get_queryset(self):
		return Question.objects.filter(
			pub_date__lte=timezone.now()
		).order_by('-pub_date')[:5]

	def get_context_data(self, **kwargs):
		# Call the base implementation first to get the context
		context = super(IndexView, self).get_context_data(**kwargs)
		
		# Create any data and add it to the context
		num_visits = self.request.session.get('num_visits',0)
		self.request.session['num_visits'] = num_visits+1
		context['num_visits'] = num_visits
		
		return context

class DetailView(generic.DetailView):
	model = Question
	template_name = 'polls/detail.html'

	def get_queryset(self):
		return Question.objects.filter(pub_date__lte=timezone.now())

class ResultsView(generic.DetailView):
	model = Question
	template_name = 'polls/results.html'

def vote(request, question_id):
	question = get_object_or_404(Question, pk=question_id)
	try:
		selected_choice = question.choice_set.get(pk=request.POST['choice'])
	except (KeyError, Choice.DoesNotExist):
		# Redisplay the question voting form.
		return render(request, 'polls/detail.html', {
			'question': question,
			'error_message': "You didn't select a choice.",
		})
	else:
		selected_choice.votes += 1
		selected_choice.save()
		# Always return an HttpResponseRedirect after successfully dealing
		# with POST data. This prevents data from being posted twice if a
		# user hits the Back button.
		return HttpResponseRedirect(reverse('polls:results', args=(question.id,)))


