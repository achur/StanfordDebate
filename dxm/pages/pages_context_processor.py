import settings

def constants(request):
    return {
               'CONSTANTS': settings.CONSTANTS,
           }
