from django.shortcuts import render

# Create your views here.
from django.http import JsonResponse





def hashtag_posts_view(request, tag):
    hashtag = hashtag.objects.filter(name=tag).first()
    if not hashtag:
        posts = []
    else:
        posts = hashtag.posts.select_related("user").prefetch_related("images")

        return render(request, "hashtag/hashtag_feed.html",{
            "hashtag":tag,
            "posts":posts
        })
    
    
def hashtag_suggestions(request):
    q = request.GET.get("q","")

    tags = Hashtag.objects.filter(name_icontains=q)[10]

    data = [{"name":tag.name} for tag in tags]

    return JsonResponse(data, safe=False)