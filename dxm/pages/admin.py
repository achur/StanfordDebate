from pages.models import Member, Tournament, Result, Officers, FAQ, PotentialMember
from django.contrib import admin

class TournamentAdmin(admin.ModelAdmin):
    ordering = ['startdate',]
    list_display = ('name', 'startdate')

class MemberAdmin(admin.ModelAdmin):
    ordering = ['name',]
    list_display = ('name', 'year', 'email')

admin.site.register(Member, MemberAdmin)
admin.site.register(Tournament, TournamentAdmin)
admin.site.register(Result)
admin.site.register(Officers)
admin.site.register(FAQ)
admin.site.register(PotentialMember)