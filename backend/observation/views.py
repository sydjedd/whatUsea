from django.core import serializers
from django.http import JsonResponse
from django.views.decorators.http import require_http_methods
from django.views.decorators.csrf import csrf_exempt
from django.db.models import F, Q
from datetime import datetime
from observation.models import Observation
from referential.models import Quality, Species


@require_http_methods(['POST', 'GET', 'PUT', 'DELETE'])
@csrf_exempt
def Main(request, id = None):
    if not id:
        if request.method == 'GET':
            return GetAll(request)
        if request.method == 'POST':
            return Create(request)
    else:
        if request.method == 'GET':
            return GetByID(request, id)
        elif request.method == 'PUT':
            return UpdateByID(request, id)
        elif request.method == 'DELETE':
            return DeleteByID(request, id)

@require_http_methods(['GET'])
@csrf_exempt
def GetAll(request):
    species = request.GET.get('species', None)
    if species:
        filter = Q(species = species)
    else:
        filter = Q()

    return JsonResponse({
        'status' : 'success',
        'data' : {
            'observation' : list(
                Observation.objects
                    .values('id', 'ilot', 'ilot_distance', 'date_time', 'quality', 'species', 'mammel_apnea_duration', 'animal_length', 'fish_single', 'fish_number')
                    .annotate(family = F('species__family'))
                    .filter(filter)
            )
        },
        'message' : ''
    }, safe = False)

@require_http_methods(['POST'])
@csrf_exempt
def Create(request):
    # Contrôle des données
    # TODO Gérer les erreurs séparément pour un message d'erreur plus explicite, utiliser Regex etc.
    error = {}
    observation = Observation()
    observation, error = DataControl(observation, request.PUT)

    if error:
        return JsonResponse({
            'status' : 'fail',
            'data' : error,
            'message' : ''
        }, safe = False)

    try:
        observation.save()
        return JsonResponse({
            'status' : 'success',
            'data' : {},
            'message' : 'Enregistrement créé avec succès'
        }, safe = False)
    except:
        return JsonResponse({
            'status' : 'error',
            'data' : {},
            'message' : 'Erreur lors de la création'
        }, safe = False)

@require_http_methods(['GET'])
@csrf_exempt
def GetByID(request, id):
    observation = (
        Observation.objects
            .values('id', 'ilot', 'ilot_distance', 'date_time', 'quality', 'species', 'mammel_apnea_duration', 'animal_length', 'fish_single', 'fish_number')
            .annotate(family = F('species__family'))
            .filter(id = id)
    )

    if not observation.count():
        return JsonResponse({
            'status' : 'fail',
            'data' : {},
            'message' : 'Aucun résultat'
        }, safe = False)

    return JsonResponse({
        'status' : 'success',
        'data' : {
            'observation' : list(observation)[0]
        },
        'message' : ''
    }, safe = False)

@require_http_methods(['PUT'])
@csrf_exempt
def UpdateByID(request, id):
    # Hack pour la récupération des données
    if hasattr(request, '_post'):
        del request._post
        del request._files
    try:
        request.method = "POST"
        request._load_post_and_files()
        request.method = "PUT"
    except AttributeError:
        request.META['REQUEST_METHOD'] = 'POST'
        request._load_post_and_files()
        request.META['REQUEST_METHOD'] = 'PUT'
    request.PUT = request.POST

    # Contrôle des données
    # TODO Gérer les erreurs séparément pour un message d'erreur plus explicite, utiliser Regex etc.
    error = {}
    observation = Observation.objects.get(id = id)
    observation, error = DataControl(observation, request.PUT)

    if error:
        return JsonResponse({
            'status' : 'fail',
            'data' : error,
            'message' : ''
        }, safe = False)

    try:
        observation.save()
        return JsonResponse({
            'status' : 'success',
            'data' : {},
            'message' : 'Enregistrement modifié avec succès'
        }, safe = False)
    except:
        return JsonResponse({
            'status' : 'error',
            'data' : {},
            'message' : 'Erreur lors de la modification'
        }, safe = False)

@require_http_methods(['DELETE'])
@csrf_exempt
def DeleteByID(request, id):
    try:
        Observation.objects.get(id = id).delete()
        return JsonResponse({
            'status' : 'success',
            'data' : {},
            'message' : 'Enregistrement supprimé avec succès'
        }, safe = False)
    except:
        return JsonResponse({
            'status' : 'fail',
            'data' : {},
            'message' : 'Erreur lors de la suppression'
        }, safe = False)


def DataControl(observation, data):
    error = {}
    # Îlot ID
    observation.ilot = data.get('ilot', None)
    if not observation.ilot:
        error['ilot'] = 'Obligatoire'

    # Îlot distance
    observation.ilot_distance = data.get('ilot_distance', None)
    if not observation.ilot_distance:
        error['ilot_distance'] = 'Obligatoire'
    elif not PositifInt(observation.ilot_distance):
        error['ilot_distance'] = 'Entier > 0'

    # Date et heure de l'observation
    date_time = data.get('date_time', None)
    if not date_time:
        error['date_time'] = 'Obligatoire'
    else:
        try:
            datetime.strptime(date_time, '%Y-%m-%d %H:%M:%S')
            observation.date_time = date_time
        except ValueError:
            error['date_time'] = 'Format attendu YYYY-MM-DD HH:MM:SS'

    # Qualité de l'observation
    quality = data.get('quality', None)
    if not quality:
        error['quality'] = 'Obligatoire'
    else:
        try:
            observation.quality = Quality.objects.get(id = quality)
        except:
            error['quality'] = 'ID inconnu'

    # Espèce
    species = data.get('species', None)
    if not species:
        error['species'] = 'Obligatoire'
    else:
        try:
            observation.species = Species.objects.get(id = species)
        except:
            error['species'] = 'ID inconnu'

    # Famille
    if 'species' not in error:
        # Mamifere
        if observation.species.family.id == 1:
            # Taille
            observation.animal_length = data.get('animal_length', None)
            if not observation.animal_length:
                error['animal_length'] = 'Obligatoire si species.family = 1'
            elif not PositifInt(observation.animal_length):
                error['animal_length'] = 'Entier > 0'
            # Temps apnée
            observation.mammel_apnea_duration = data.get('mammel_apnea_duration', None)
            if not observation.mammel_apnea_duration:
                error['mammel_apnea_duration'] = 'Obligatoire si species.family = 1'
            elif not PositifInt(observation.mammel_apnea_duration):
                error['mammel_apnea_duration'] = 'Entier > 0'
        # Poisson
        elif observation.species.family.id == 2:
            # Seul ou banc
            fish_single = data.get('fish_single', None)
            if not fish_single:
                error['fish_single'] = 'Obligatoire'
            elif fish_single not in ('True', 'False'):
                error['fish_single'] = 'Valeurs attendues True ou False'
            else:
                observation.fish_single = bool(fish_single)
                # Seul
                if fish_single == 'True':
                    observation.animal_length = data.get('animal_length', None)
                    if not observation.animal_length:
                        error['animal_length'] = 'Obligatoire si species.family = 2 et fish_single = True'
                    elif not PositifInt(observation.animal_length):
                        error['animal_length'] = 'Entier > 0'
                # Banc
                else:
                    observation.fish_number = data.get('fish_number', None)
                    if not observation.fish_number:
                        error['fish_number'] = 'Obligatoire si species.family = 2 et fish_single = False'
                    elif not PositifInt(observation.fish_number):
                        error['fish_number'] = 'Entier > 0'

    return observation, error

def PositifInt(string):
    try:
        number = int(string)
    except:
        return False

    if number <= 0:
        return False

    return True
