from django.shortcuts import redirect, render
from .models import Food, Consume



# Create your views here.
def index(request):
    foods = Food.objects.all()
    consumed_food = []

    if request.method == "POST":
        food_consumed = request.POST.get('food_consumed')
        try:
            food = Food.objects.get(name=food_consumed)
        except Food.DoesNotExist:
            food = None

        if food:
            user = request.user if request.user.is_authenticated else None
            Consume.objects.create(user=user, food_consumed=food)

        return redirect(request.path_info)

    if request.user.is_authenticated:
        consumed_food = Consume.objects.filter(user=request.user)
    else:
        consumed_food = Consume.objects.filter(user=None)

    calorie_goal = request.GET.get('calorie_goal', 2000)
    try:
        calorie_goal = int(calorie_goal)
    except ValueError:
        calorie_goal = 2000

    return render(request, 'myapp/index.html', {
        'foods': foods,
        'consumed_food': consumed_food,
        'calorie_goal': calorie_goal,
    })


def delete_consume(request, id):
    consumed_food = Consume.objects.get(id=id)
    calorie_goal = request.GET.get('calorie_goal', 2000)
    if request.method == 'POST':
        consumed_food.delete()
    return redirect(f"/?calorie_goal={calorie_goal}")


def delete_all_consumed(request):
    calorie_goal = request.GET.get('calorie_goal', 2000)
    consumed_food = Consume.objects.all()
    if request.method == 'POST':
        consumed_food.delete()
        return redirect(f"/?calorie_goal={calorie_goal}")
    return render(request, 'myapp/delete_all.html')

