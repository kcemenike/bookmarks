from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.shortcuts import get_object_or_404
from django.http import JsonResponse, HttpResponse
from django.views.decorators.http import require_POST
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

from .models import Image
from .forms import ImageCreateForm
from bookmarks.common.decorators import ajax_required
from actions.utils import create_action

import redis
from django.conf import settings

# connect to redis
r = redis.Redis(host=settings.REDIS_HOST,
                port=settings.REDIS_PORT,
                db=settings.REDIS_DB)


# Create your views here.
@login_required
def image_create(request):
    if request.method == "POST":
        # form is sent
        form = ImageCreateForm(data=request.POST)
        if form.is_valid():
            # form data is valid
            cd = form.cleaned_data
            new_item = form.save(commit=False)

            # assign current user to the item
            new_item.user = request.user
            # save
            new_item.save()

            # create action
            create_action(request.user, 'bookmarked image', new_item)

            # display success message
            messages.success(request, 'Image added successfully')

            # redirect to new created item detail_view
            return redirect(new_item.get_absolute_url())
    else:
        # build form with data provided by the bookmarklet via GET
        form = ImageCreateForm(data=request.GET)

    return render(request,
                  'images/image/create.html',
                  {'section': 'images', 'form': form})


def image_detail(request, id, slug):
    image = get_object_or_404(Image, id=id, slug=slug)
    # increment total image views by 1 in redis DB
    total_views = r.incr(f"image:{image.id}:views")  # object-type:id:field

    # increment image ranking by 1
    r.zincrby('image_ranking', 1, image.id)

    return render(request,
                  'images/image/detail.html',
                  {'section': 'image', 'image': image, 'total_views': total_views})


@ajax_required
@login_required
@require_POST
def image_like(request):
    image_id = request.POST.get('id')
    action = request.POST.get('action')
    if image_id and action:
        try:
            image = Image.objects.get(id=image_id)
            if action == 'like':
                image.users_like.add(request.user)
                # record activity
                create_action(request.user, 'likes', image)
            else:
                image.users_like.remove(request.user)
            return JsonResponse({'status': 'ok'})
        except:
            pass
    return JsonResponse({'status': 'error'})


@login_required
def image_list(request):
    images = Image.objects.all()
    paginator = Paginator(images, 15)
    page = request.GET.get('page')
    try:
        images = paginator.page(page)
    except PageNotAnInteger:
        # If page is not an integer, deliver the first page
        images = paginator.page(1)
    except EmptyPage:
        # if page is out of range and page is ajax, return an empty page
        if request.is_ajax():
            return HttpResponse('')
        # if page is not ajax, deliver last page
        image = paginator.page(paginator.num_pages)
    if request.is_ajax():
        return render(request,
                      'images/image/list_ajax.html',
                      {'section': 'images', 'images': images})

    return render(request,
                  'images/image/list.html',
                  {'section': 'images', 'images': images})


@login_required
def image_ranking(request):
    # get image ranking dictionary from redis and their ranking
    image_ranking = r.zrange('image_ranking', 0, -1,
                             desc=True, withscores=True)[:10]
    image_ranking_ids = [int(id[0]) for id in image_ranking]
    rank = [int(id[1]) for id in image_ranking]

    # get most viewed images and sort using image_ranking_ids as keys
    most_viewed = list(Image.objects.filter(id__in=image_ranking_ids))
    most_viewed.sort(key=lambda x: image_ranking_ids.index(x.id))

    ranking = dict(zip(most_viewed, rank))
    return render(request,
                  'images/image/ranking.html',
                  {'section': 'images', 'ranking': ranking})
