from django.shortcuts import render, redirect
from django.http.response import HttpResponse, JsonResponse
from .models import *
import random


# {
#     'status': True,
#     'data': [
#         {},
#     ]
# }

# Create your views here.
def home(request):
    context = {'categories': Category.objects.all()}

    # redirect when a category is selected
    if request.GET.get('category'):
        return redirect(f"/quiz/?category={request.GET.get('category')}")

    return render(request, 'home.html', context)


def quiz(request):
    context = {'category': request.GET.get('category')}

    return render(request, 'quiz.html', context)


def get_quiz(request):
    try:
        # Get all questions from the Question table
        # question_objs = list(Question.objects.all())
        question_objs = Question.objects.all()

        # Get questions according to category
        if request.GET.get('category'):
            question_objs = question_objs.filter(category__category_name__icontains=request.GET.get('category'))

        # Create list object
        question_objs = list(question_objs)

        # randomize the results
        random.shuffle(question_objs)


        # Create Json objects
        data = []
        for question_obj in question_objs:
            data.append({
                "uid": question_obj.uid,
                "category":question_obj.category.category_name,
                "question":question_obj.question,
                "marks":question_obj.marks,
                "answers": question_obj.get_answers()
            })

        payload = {'status':True, 'data':data}

        return JsonResponse(payload)

    except Exception as e:
        print(e)

    return HttpResponse('Something went wrong')