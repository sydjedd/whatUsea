from django.http import JsonResponse
from django.views.decorators.http import require_http_methods
from referential.models import Quality, Family, Species


@require_http_methods(['GET'])
def GetAll(request):
    return JsonResponse({
        'status' : 'success',
        'data' : {
            'quality' :
                list(
                    Quality.objects
                        .values('id', 'libelle')
                        .order_by('libelle')
                ),
            'family' :
                list(
                    Family.objects
                        .values('id', 'libelle')
                        .order_by('libelle')
                ),
            'species' :
                list(
                    Species.objects
                        .values('id', 'libelle', 'family')
                        .order_by('libelle')
                )
        },
        'message' : ''
    }, safe = False)

@require_http_methods(['GET'])
def GetQuality(request):
    return JsonResponse({
        'status' : 'success',
        'data' : {
            'quality' :
                list(
                    Quality.objects
                        .values('id', 'libelle')
                        .order_by('libelle')
                )
        },
        'message' : ''
    }, safe = False)

@require_http_methods(['GET'])
def GetFamily(request):
    return JsonResponse({
        'status' : 'success',
        'data' : {
            'family' :
                list(
                    Family.objects
                        .values('id', 'libelle')
                        .order_by('libelle')
                )
        },
        'message' : ''
    }, safe = False)

@require_http_methods(['GET'])
def GetSpecies(request):
    return JsonResponse({
        'status' : 'success',
        'data' : {
            'species' :
                list(
                    Species.objects
                        .values('id', 'libelle', 'family')
                        .order_by('libelle')
                )
        },
        'message' : ''
    }, safe = False)
