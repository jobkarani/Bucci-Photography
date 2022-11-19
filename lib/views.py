from django.shortcuts import render, get_object_or_404, redirect, render
from django.template.loader import render_to_string
from django.views.decorators.csrf import csrf_exempt
import json
from .models import LibGroup, Technique, Location, Category, Image


# Create your views here.
def libs(request):
    lib_groups = LibGroup.objects.all().order_by('title')
    categories = Category.objects.all()
    location = Location.objects.all()
    images = Image.objects.all()

    context = {
        'libGroups': lib_groups, 
        'categories':categories, 
        'location':location, 
        'images':images
        }

    return render(request, 'lib/libs.html', context)


def lib_detail(request, lib_title_slug):
    context_dict = {}

    try:
        lib_groups = LibGroup.objects.get(slug=lib_title_slug)
        context_dict['libGroups'] = lib_groups
        techniques = technique.objects.filter(group=lib_groups).order_by('published_date')
        context_dict['techniques'] = techniques

    except LibGroup.DoesNotExist:
        pass

    return render(request, 'lib/lib_detail.html', context_dict)


def craft_detail(request, craft_id):
    categories = Category.objects.all()
    location = Location.objects.all()
    technique = get_object_or_404(Technique, id=craft_id)

    try:
        next_technique = technique.get_next_by_published_date()
        while next_technique.group != technique.group:
            next_technique = next_technique.get_next_by_published_date()
    except Technique.DoesNotExist:
        next_technique = None

    try:
        previous = technique.get_previous_by_published_date()
        while previous.group != technique.group:
            previous = previous.get_previous_by_published_date()
    except Technique.DoesNotExist:
        previous = None

    context = {
        'technique':technique, 
        'next':next_technique, 
        'previous':previous, 
        'categories':categories,
        'location':location
        }

    return render(request, 'lib/craft_detail.html', context)


def about_me(request):
    categories = Category.objects.all()
    location = Location.objects.all()

    context = {
        'categories':categories,
        'location':location
        }

    return render(request, 'lib/about_me.html', context)


def all_images(request):
    images = Image.objects.all()
    categories = Category.objects.all()
    location = Location.objects.all()

    context = {
        'images':images,
        'categories':categories,
        'location':location
        }

    return render(request,'lib/libs.html',context)


def image_by_location(request, location):
    # if request.method == "GET" and 'location_name' in request.GET and request.is_ajax():
    #     location = request.GET['location_name']
    #     categories = Category.objects.all()
    #     location = Location.objects.all()
    #     images_location = Image.get_image_by_location(location)

    #     return render('lib/location.html', {'images_location':images_location, 'categories':categories,'location':location})

    # return redirect(all_images)
    images = Image.get_image_by_location(location)
    categories = Category.objects.all()
    location = Location.objects.all()

    context = {
        'images_location':images, 
        'categories':categories,
        'location':location
        }
    return render(request, 'lib/location.html', context )

def image_by_category(request, category):
    if request.method == "GET" and 'category_name' in request.GET and request.is_ajax():
        category = request.GET['category_name']
    categories = Category.objects.all()
    location = Location.objects.all()
    images_category = Image.get_image_by_category(category)

    context = {
        'images_category':images_category, 
        'categories':categories,
        'location':location
        }

    return render(request, 'lib/category.html',context)


def display_details(request,image_id):
    categories = Category.objects.all()
    location = Location.objects.all()
    this_image = Image.get_image_by_id(image_id)

    context = {
        'this_image':this_image,
        'categories':categories,
        'location':location
        }

    return render(request,'lib/image.html',context)


def search_image(request):
    categories = Category.objects.all()
    location = Location.objects.all()
    
    if 'image-search' in request.GET and request.GET['image-search']:
        search_category = request.GET.get('image-search')
        images_result = Image.get_image_by_category(search_category)
        message = f'{search_category}'

        context = {
            'images_result':images_result,
            'message':message,
            'categories':categories,
            'location':location
            }

        return render(request,'lib/search.html',context)

    else:

        context = {
            'categories':categories,
            'location':location
            }
        return render(request,'lib/search.html',context)