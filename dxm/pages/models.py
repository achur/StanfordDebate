from django.db import models

from lib.gfm import downmark

from templatetags.pages_tags import member_listify

months_of_year = ["January", "February", "March", "April", "May", "June", "July", "August", "September", "October", "November", "December"]
def stringify_date_range(startdate, enddate):
    sameyear = (startdate.year == enddate.year)
    samemonth = (startdate.month == enddate.month)
    sameday = (startdate.day == enddate.day)
    if not sameyear:
        return "" + months_of_year[startdate.month - 1] + " " + str(startdate.day) + ", " + str(startdate.year) \
               + " - " + "" + months_of_year[enddate.month - 1] + " " + str(enddate.day) + ", " + str(enddate.year)
    if not samemonth:
        return "" + months_of_year[startdate.month - 1] + " " + str(startdate.day) + " - " \
               + months_of_year[enddate.month - 1] + " " + str(enddate.day) + ", " + str(enddate.year)
    if not sameday:
        return "" + months_of_year[startdate.month - 1] + " " + str(startdate.day) + " - "\
           + str(enddate.day) + ", " + str(enddate.year)
    return "" + months_of_year[startdate.month - 1] + " " + str(startdate.day) + ", " + str(startdate.year)
    

class Member(models.Model):
    name = models.CharField('member name', max_length=50)
    email = models.CharField('member email', max_length=50)
    year = models.IntegerField('member class year')
    active = models.BooleanField('is active')
    def __unicode__(self):
        return self.name + " -- " + str(self.year)

# Officers is a singleton model (there is only
# one set of models at any given point) so
# we override the save and delete methods
class Officers(models.Model):
    president = models.ManyToManyField(Member, verbose_name='President(s)', related_name='president_set')
    apdacaptain = models.ManyToManyField(Member, verbose_name='APDA Captain(s)', related_name='apdacaptains')
    ndtcaptain = models.ManyToManyField(Member, verbose_name='NDT Captain(s)', related_name='ndtcaptains')
    treasurer = models.ManyToManyField(Member, verbose_name='Treasurer(s)', related_name='treasurers')
    hstd = models.ManyToManyField(Member, verbose_name='High School Tournament Director(s)', related_name='hstds')
    xr = models.ManyToManyField(Member, verbose_name='External Relations', related_name='xrs')
    ctd = models.ManyToManyField(Member, verbose_name='College Tournament Director(s)', related_name='ctds')
    socialchair = models.ManyToManyField(Member, verbose_name='Social Chair(s)', related_name='socialchairs')
    webmaster = models.ManyToManyField(Member, verbose_name='Webmaster(s)', related_name='webmasters')
    year = models.IntegerField('year elected')
    def save(self):
        self.id=self.year
        super(Officers, self).save()
    def delete(self):
        pass
    def __unicode__(self):
        return "" + str(self.year) + "-" + str(self.year + 1) + " officers"
    class Meta:
        verbose_name = 'List of officers'
        verbose_name_plural = 'List of officers'

class Tournament(models.Model):
    name = models.CharField('name of tournament', max_length=100)
    startdate = models.DateField('start date')
    enddate = models.DateField('end date')
    def formatdate(self):
        return stringify_date_range(self.startdate, self.enddate)
    def __unicode__(self):
        return self.name
    
class Result(models.Model):
    tournament = models.ForeignKey(Tournament, related_name='results')
    team = models.ManyToManyField(Member, verbose_name='team members')
    rank = models.CharField('team rank', max_length=35)
    def __unicode__(self):
        return self.tournament.name + " -- " + member_listify(self.team.all(), False) + " -- " + self.rank

class FAQ(models.Model):
    question = models.CharField('question', max_length=1000)
    answer = models.CharField('answer', max_length=1000)
    def richquestion(self):
        return downmark(question)
    def richanswer(self):
        return downmark(answer)
    def __unicode__(self):
        return self.question

class PotentialMember(models.Model):
    name = models.CharField('name', max_length=50)
    email = models.CharField('email', max_length=50)
    note = models.CharField('additional note', max_length=1000)
    def __unicode__(self):
        return self.name + " -- " + self.email
