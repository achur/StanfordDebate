from django import template

register = template.Library()

def wrapMember(member, hotlink):
    if hotlink and hotlink != 'False':
        return '<a href="mailto:' + member.email + '">' + member.name + '</a>'
    elif hotlink == 'False':
        return '<a>' + member.name + '</a>'
    else:
        return member.name

def member_listify(members, hotlink):
    num = len(members)
    if(num <= 0):
        return "No members listed!"
    strlist = wrapMember(members[0], hotlink)
    if(num == 1):
        return strlist
    for i in range(1, num - 1):
        strlist += (", " + wrapMember(members[i], hotlink))
    strlist += (" and " + wrapMember(members[num - 1], hotlink))
    return strlist

register.simple_tag(member_listify)