from django.shortcuts import render

# Create your views here.
# make ps_list View
def ps_list(request):
    return render(request, 'tail_docker_ps/ps_list.html', {})