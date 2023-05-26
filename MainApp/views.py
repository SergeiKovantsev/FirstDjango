from django.shortcuts import render, HttpResponse, redirect
from django.http import HttpResponseNotFound
from django.core.exceptions import ObjectDoesNotExist
from MainApp.models import Item, Color

author = {
    "name": "Сергей",
    "surname": "Алексеевич",
    "family": "Кованцев",
    "phone": "8-961-298-50-49",
    "email": "s.kovantsev@gmail.com",
}

# Create your views here.
def home(request):
    context = {
        "name": author['name'],
        "surname": author['surname'],
        "family": author['family']
    }
    return render(request, 'index.html', context)


def about(request):
    context = {
        'author': author
    }
    return render(request, 'about.html', context)


def item_page(request, id):
    try:
        item = Item.objects.get(id=id)
    except ObjectDoesNotExist:
        return HttpResponseNotFound(f"Товар с id={id} не найден")

    context = {
        'item': item
    }
    return render(request, 'item-page.html', context)


def items_list(request):
    items = Item.objects.all()
    context = {
        'items': items
    }
    return render(request, 'item-list.html', context)


def item_add(request):
    if request.method == "GET":
        colors = Color.objects.all()
        context = {
            "colors": colors
        }
        return render(request, "item-add.html", context)


# Получаем данные от формы
def item_create(request):
    if request.method == "POST":
        form_data = request.POST
        print(f"{form_data=}")
        item = Item(
            name=form_data['name'],
            brand=form_data['brand'],
            count=form_data['count'],
        )
        item.save()

        colors_id = form_data.getlist("colors_id")
        for color_id in colors_id:
            color = Color.objects.get(id=color_id)
            item.colors.add(color)
            # item.save()
        return redirect('items-list')