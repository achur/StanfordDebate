from pages.models import Member, Tournament, Result, Officers, FAQ, PotentialMember, AdditionalPosition
from django.contrib import admin

class TournamentAdmin(admin.ModelAdmin):
    list_display = ('name', 'startdate')

class MemberAdmin(admin.ModelAdmin):
    list_display = ('name', 'year', 'email')

class FAQAdmin(admin.ModelAdmin):
    list_display = ('question', 'answer')

admin.site.register(Member, MemberAdmin)
admin.site.register(Tournament, TournamentAdmin)
admin.site.register(Result)
admin.site.register(Officers)
admin.site.register(AdditionalPosition)
admin.site.register(FAQ, FAQAdmin)
admin.site.register(PotentialMember)