from django.shortcuts import render,render_to_response
from django.contrib.auth.decorators import login_required

@login_required
def index(request):
    context = {}
    # The template to be loaded as per gentelella.
    # All resource paths for gentelella end in .html.

    # Pick out the html file name from the url. And load that template.
    # load_template = request.path.split('/')[-1]
    # template = loader.get_template('app/' + load_template)
    # return HttpResponse(template.render(context, request))

    return render_to_response('dashboard/index.html',{'request':request})
