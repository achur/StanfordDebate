import settings

def constants(request):
    return {
               'CONSTANTS': settings.CONSTANTS,
               'BASE_URL': settings.BASE_URL
           }
