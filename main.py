#roomchecker could easily return an address
# do i even need the name?
#room# is after IDENTIFICATION
#Name is after ___,
#HH# is 9 digits followed by a word for tier

import fitz
import re
import datetime
import time
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.pdfbase.pdfmetrics import registerFont
from reportlab.pdfgen.canvas import Canvas
from reportlab.lib.colors import green
from reportlab.lib.units import inch


fname = 'C:\python35\Alejandro.xps'
doc = fitz.open(fname)
page_count = doc.pageCount
guest_list = []

class GuestKey:
    def __init__(self, name, room, hhonors, checkout):
        self.name = name
        self.room = room
        self.hhonors = hhonors
        self.checkout = checkout

def DateChecker(text):
    today = datetime.datetime.today()
    date_reg_exp = re.compile('\d{1,2}/\d{1,2}/\d{4}')
    matches = date_reg_exp.findall(text)
    for word in matches:
        zword = datetime.datetime.strptime(word,'%m/%d/%Y')
        if zword > today:
            return word

def HonorsChecker(text):
    hh_pattern = re.compile('\d{9}')
    try:
        honor_num = hh_pattern.search(text).group()
        return honor_num
    except:
        return 'N/A'

def RoomChecker(text):
    location = text.index('IDENTIFICATION')
    room_pattern = re.compile('[1-4][0-7][0-9]')
    room_num = room_pattern.search(text[location:(location+25)]).group()
    if room_num is not None:
        return room_num
    else:
        return 'N/A'

def NameChecker(text):
    pass

def PageParser(text,i):
    checkout = DateChecker(text)
    hhonors = HonorsChecker(text)
    room = RoomChecker(text)
    name = i
    return (name,hhonors,room,checkout)


for i in range(page_count):
    page = doc.loadPage(i)
    text = page.getText(output = "text").replace('\n',' ')
    name,hhonors,room,checkout = PageParser(text,i)
    guest = GuestKey(name,room,hhonors,checkout)
    guest_list.append(guest)

registerFont(TTFont("Vera", "Vera.ttf"))
registerFont(TTFont("VeraBI", "VeraBI.ttf"))
c = Canvas('KeyPacket.pdf', pagesize=(612,792))
c.setFont('Vera', 10)

for i in range(len(guest_list)):
    room, hhonors, checkout, name = guest_list[i].room, guest_list[i].hhonors, guest_list[i].checkout, guest_list[i].name
    #print(guest_list[i].name,guest_list[i].room,guest_list[i].hhonors,guest_list[i].checkout)
    c.showPage()
    c.saveState()
    c.rotate(90)
    c.drawString(720,-360, (room))
    c.drawString(720,-396, (checkout))
    c.drawString(604,-198, (hhonors))
    c.restoreState()


c.save()
