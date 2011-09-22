from django.http import HttpResponse
from django.shortcuts import render_to_response
from django.template import RequestContext
from pages.models import Tournament, Result, PotentialMember, Officers, Member, FAQ, AdditionalPositions
from flatblocks.models import FlatBlock
from settings import CONSTANTS
import datetime
from lib.gfm import downmark

def curYear():
    today = datetime.date.today()
    if today < datetime.date(today.year, CONSTANTS['cutoffMonth'], 1):
        year = today.year - 1
    else:
        year = today.year
    return year

def getTournamentYearList():
    years = [t.year for t in Tournament.objects.dates('startdate', 'year')]
    minyear = min(years) - 1 # might be, say Apr. 1, 2010, which goes in 2009-2010
    maxyear = max(years)
    return range(minyear, maxyear + 1)

def mainpage(request):
    return render_to_response('mainpage.html', context_instance=RequestContext(request))

def resources(request):
    return render_to_response('resources.html', context_instance=RequestContext(request))

def links(request):
    return render_to_response('links.html', context_instance=RequestContext(request))

def join(request):
    return render_to_response('join.html', context_instance=RequestContext(request))

# Creates a new potential user and saves it
# to the database.  Designed for AJAX.
def joincreate(request):
    newname = request.POST["name"] if "name" in request.POST else (request.GET["name"] if "name" in request.GET else "")
    newemail = request.POST["email"] if "email" in request.POST else (request.GET["email"] if "email" in request.GET else "")
    newnote = request.POST["note"] if "note" in request.POST else (request.GET["note"] if "note" in request.GET else "")
    PotentialMember.objects.create(name=newname, email=newemail, note=newnote)
    return HttpResponse("OK")


def tournamentsForDateRange(startmonth, startyear, endmonth, endyear):
    endmin = datetime.date(startyear, startmonth, 1)
    if (endmonth < 12):
        startmax = datetime.date(endyear, endmonth + 1, 1)
    else:
        startmax = datetime.date(endyear + 1, 1, 1)
    return Tournament.objects.filter(enddate__gte=endmin, startdate__lt=startmax).order_by('startdate')

def resultsForYear(year):
    tournaments = tournamentsForDateRange(CONSTANTS['cutoffMonth'], year, CONSTANTS['cutoffMonth'] - 1, year + 1).reverse()
    return [ { "tournament": t, "results": t.results.all() } for t in tournaments ]

def results(request):
    dict = {}
    if ("year" in request.GET):
        year = int(request.GET["year"])
        dict["tournaments"] = resultsForYear(year)
    else:
        # Default to showing last year and current year results
        year = curYear()
        tournaments = tournamentsForDateRange(CONSTANTS['cutoffMonth'], year - 1, CONSTANTS['cutoffMonth'] - 1, year + 1).reverse()
        dict["tournaments"] = [ { "tournament": t, "results": t.results.all() } for t in tournaments ]
    dict["year"] = (str(year) + " - " + str(year+1))
    years = [{"year": (str(y) + " - " + str(y+1)), "val": str(y)} for y in getTournamentYearList() if y <= curYear()]
    years.reverse()
    dict["years"] = years
    return render_to_response('results.html', dict, context_instance=RequestContext(request))

def scheduleForYear(year):
    return tournamentsForDateRange(CONSTANTS['cutoffMonth'], year, CONSTANTS['cutoffMonth'] - 1, year + 1)

def schedule(request):
    dict = {}
    if ("year" in request.GET):
        year = int(request.GET["year"])
    else:
        year = curYear()
    dict["year"] = (str(year) + " - " + str(year+1))
    dict["tournaments"] = scheduleForYear(year)
    years = [{"year": (str(y) + " - " + str(y+1)), "val": str(y)} for y in getTournamentYearList()]
    years.reverse()
    dict["years"] = years
    return render_to_response('schedule.html', dict, context_instance=RequestContext(request))

def officerFormatList(officers):
    return [
                [ #eboard
                    { "title": "President" if len(officers.president.all()) == 1 else "Presidents", "name": officers.president.all()},
                    { "title": "APDA Captain" if len(officers.apdacaptain.all()) == 1 else "APDA Captains", "name": officers.apdacaptain.all()},
                    { "title": "NDT Captain" if len(officers.ndtcaptain.all()) == 1 else "NDT Captains", "name": officers.ndtcaptain.all()},
                    { "title": "Treasurer" if len(officers.treasurer.all()) == 1 else "Treasurers", "name": officers.treasurer.all()},
                    { "title": "High School Tournament Director" if len(officers.hstd.all()) == 1 else "High School Tournament Directors", "name": officers.hstd.all()},
                ],
                [
                    { "title": "External Relations", "name": officers.xr.all()},
                    { "title": "College Tournament Director" if len(officers.ctd.all()) == 1 else "College Tournament Directors", "name": officers.ctd.all()},
                    { "title": "Social Chair" if len(officers.socialchair.all()) == 1 else "Social Chairs", "name": officers.socialchair.all()},
                    { "title": "Webmaster" if len(officers.webmaster.all()) == 1 else "Webmasters", "name": officers.webmaster.all()}
                ]
            ]

def roster(request):
    dict = {}
    officers = Officers.objects.get(year=curYear())
    officerlist = officerFormatList(officers)
    dict["eboard"] = officerlist[0]
    other_officers = officerlist[1]
    additional_positions = AdditionalPositions.objects.filter(year=curYear())
    for position in additional_positions:
        other_officers.append( { "title": position.title, "name": position.members } )
    dict["other_officers"] = other_officers
    members = Member.objects.filter(active=True).order_by('year', 'name')
    spacedmembers = [members[0]]
    for i in range(1, len(members)):
        if members[i-1].year != members[i].year:
            spacedmembers.append( { "year": "", "name": "" })
        spacedmembers.append(members[i])
    dict["members"] = spacedmembers
    return render_to_response('roster.html', dict, context_instance=RequestContext(request))

def faq(request):
    dict = {}
    dict["faqs"] = FAQ.objects.all()
    return render_to_response('faq.html', dict, context_instance=RequestContext(request))

# Simple flat pages served from the database
def pages(request, slug_name):
    dict = {}
    block = FlatBlock.objects.get(slug=slug_name)
    dict["header_data"] = block.header
    dict["content_data"] = downmark(block.content) if block.markdown else block.content
    return render_to_response('pages.html', dict, context_instance=RequestContext(request))
