from pages.models import Member, Tournament, Result, Officers, FAQ, PotentialMember, AdditionalPosition, StaffPosition
from django.contrib import admin

class TournamentAdmin(admin.ModelAdmin):
    list_display = ('name', 'startdate')

class MemberAdmin(admin.ModelAdmin):
    list_display = ('name', 'year', 'email')

class FAQAdmin(admin.ModelAdmin):
    list_display = ('question', 'answer')

class StaffPositionAdmin(admin.ModelAdmin):
    list_display = ('title',)

admin.site.register(Member, MemberAdmin)
admin.site.register(Tournament, TournamentAdmin)
admin.site.register(Result)
admin.site.register(Officers)
admin.site.register(AdditionalPosition)
admin.site.register(FAQ, FAQAdmin)
admin.site.register(PotentialMember)
admin.site.register(StaffPosition, StaffPositionAdmin)
