import urllib.request
from pyquery import PyQuery as pq
import requests
import sys

def esc(string):
    return string.replace("\"", "\"\"")

# gets the link to each individial course in a list
def get_ox_course_list():
    cl = []
    index = 0
    section_end = len(ox_page)
    while (1):
        index = ox_page.find(ox_course_marker, index+1, section_end)
        if (index < 0):
            break
        i = index
        while (ox_page[i] != "\"" and ox_page[i] != "%"):
            i = i + 1
        cl.append("https:" + ox_page[index : i] + "?wssl=1")
    return cl

# gets the info for an oxford course in a tuple (university, course title, description, reqs)
def ox_get_course_info(course_page):
    return ("University of Oxford", ox_get_name(course_page), ox_get_description(course_page), ox_get_requirements(course_page))
# puts the info into a line for writing to the CSV
def course_info_to_line(info):
    return("\"" + esc(info[0]) + "\",\"" + esc(info[1]) + "\",\"" + esc(info[2]) + "\",\"" + esc(info[3])+"\"\n")

def ox_get_name(course_page):
    doc = pq(course_page)
    return doc('title')[0].text[:doc('title')[0].text.find('|') - 1]

def ox_get_description(course_page):
    doc = pq(course_page)
    body = doc('div.field-item.even').eq(0).children().children()
    returnval = (doc('div.ui-tabs-panel').find('p'))
    return "placeholder description"

def ox_get_requirements(course_page):
    doc = pq(course_page)
    alvl = doc('div#content-tab--2').children().filter('ul').children().filter('li').eq(0).text()
    hghr = doc('div#content-tab--2').children().filter('ul').children().filter('li').eq(1).text()
    ib = doc('div#content-tab--2').children().filter('ul').children().filter('li').eq(2).text()
    return (alvl + "; " + hghr + "; " + ib)

# gets the content of the page which the URL points to
def get_page(url):
    response = requests.get(url)
    page = response.content
    return page

# the page where the oxford course listing is
ox_page_url = "https://www.ox.ac.uk/admissions/undergraduate/courses/course-listing?wssl=1"

# some strings to look for
ox_list_section_b = "page-content-container main-content"
ox_course_marker = "//www.ox.ac.uk/admissions/undergraduate/courses-listing/"
ox_list_section_e = "webform-client-form-32032"

# main
oxreq = urllib.request.Request(ox_page_url)
with urllib.request.urlopen(oxreq) as response:
   ox_page = response.read().decode()

ox_course_list = get_ox_course_list()


f = open('courses_data.csv', 'w')
f.write(course_info_to_line(("university","course","description","requirements")))
for x in ox_course_list:
    f.write(course_info_to_line(ox_get_course_info(x)))

    
