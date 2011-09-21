from pages.models import Member, Tournament, Result, Officers, FAQ, PotentialMember
from django.contrib import admin

class TournamentAdmin(admin.ModelAdmin):
    ordering = ['daysInPast',]
    list_display = ('name', 'startdate')

admin.site.register(Member)
admin.site.register(Tournament, TournamentAdmin)
admin.site.register(Result)
admin.site.register(Officers)
admin.site.register(FAQ)
admin.site.register(PotentialMember)