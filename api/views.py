import json
from datetime import date

from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt

from api.models import Person


@csrf_exempt
def create_person(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        try:
            person = Person.objects.create(iin=data['iin'], age=calculate_age(data['iin']))
        except Exception as e:
            return JsonResponse({'message': str(e)})

        return JsonResponse(person.to_json(), safe=False)


@csrf_exempt
def person_detail(request, iin):
    try:
        person = Person.objects.get(iin=iin)
    except Person.DoesNotExist as e:
        return JsonResponse({'message:': str(e)}, status=400)

    if request.method == 'GET':
        return JsonResponse(person.to_json())


def calculate_age(iin):
    today = date.today()
    born_year = iin[:2]
    if int(iin[:2]) < 21:
        born_year = int('20' + born_year)
    else:
        born_year = int('19' + born_year)
    born_month = int(iin[2:4])
    born_day = int(iin[4:6])
    return today.year - born_year - ((today.month, today.day) < (born_month, born_day))
