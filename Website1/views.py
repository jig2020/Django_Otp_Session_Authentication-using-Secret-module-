from django.http import HttpResponse,Http404
from django.shortcuts import render, get_object_or_404
from django.template import loader
from .models import AllCourses, CourseDetails

def course(request):
    ac= AllCourses.objects.all()
    template= loader.get_template('Website1/course.html')
    context = {
        'ac': ac,
    }
    return HttpResponse('')


def coursedetails(request, couse_id):
    course = get_object_or_404(AllCourses, pk=couse_id)
    coursedetails_set = course.coursedetails_set.all()
    return render(request, 'Website1/details.html', {
        'course': course,
        'coursedetails_set': coursedetails_set,
    })

def yourchoice(request, couse_id):
    course = get_object_or_404(AllCourses, pk=couse_id)
    try:
        select_coursetype = CourseDetails_set.get(pk=request.POST['choice'])
    except (KeyError, AllCourses.DoesNotExist):
        return render(request, 'Website1/details.html', {
            'course': course,
            'error_message': "select a valid option.",
        })
    else:
        select_coursetype.your_choice = True
        select_coursetype.save()
        return render(request, 'Website1/details.html', {
            'course': course,
            'select_coursetype': select_coursetype,
        })
