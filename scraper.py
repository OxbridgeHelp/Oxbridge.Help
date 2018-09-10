import urllib.request
from pyquery import PyQuery as pq
import requests
import sys
import re



def esc(string):
    return string.replace("\"", "\"\"")

# gets the link to each individial course in a list for oxford
def get_ox_course_list():
    cl = []
    index = 0
    oxreq = urllib.request.Request(ox_page_url)
    with urllib.request.urlopen(oxreq) as response:
        ox_page = response.read().decode()
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

def get_cam_course_list():
    cl = []
    page = get_page(cam_page_url)
    doc = pq(page)
    links = doc('div.view-content').find('a')
    for i in range(links.length):
        cl.append(cam_page_prefix + links.eq(i).attr('href'))
    return cl

# puts the info into a line for writing to the CSV
def course_info_to_line(info):
    return("\"" + esc(info[0]) + "\",\"" + esc(info[1]) + "\",\"" + esc(info[2]) + "\",\"" + esc(info[3])+"\"\n")

# gets the info for an oxford course in a tuple (university, course title, description, reqs)
def ox_get_course_info(course_page):
    temp = ox_get_name(course_page)
    temp2 = ''
    if (re.search('graduate', temp, re.IGNORECASE)):
        temp2 = 'Graduate course - see page for detailed requirements.'
    else:
        temp2 = ox_get_requirements(course_page)
    return ("University of Oxford", temp, ox_get_description(course_page), temp2)
def cam_get_course_info(course_page):
    temp = cam_get_name(course_page)
    temp2 = ''
    if (re.search('graduate', temp, re.IGNORECASE)):
        temp2 = 'Graduate course - see page for detailed requirements.'
    elif (re.search('II', temp, re.IGNORECASE)):
        temp2 = 'Part II course - see page for detailed requirements.'
    else:
        temp2 = cam_get_requirements(course_page)
    return ("University of Cambridge", temp, cam_get_description(course_page), temp2)

#oxford details
def ox_get_name(course_page):
    doc = pq(course_page)
    name = doc('title')[0].text[:doc('title')[0].text.find('|') - 1]
    return name
def ox_get_description(course_page):
#    doc = pq(course_page)
#    body = doc('div.field-item.even').eq(0).children().children()
#    returnval = (doc('div.ui-tabs-panel').find('p'))
    return "placeholder description"
def ox_get_requirements(course_page):
    doc = pq(course_page)
    alvl = doc('div#content-tab--2').children().filter('ul').children().filter('li').eq(0).text()
    hghr = doc('div#content-tab--2').children().filter('ul').children().filter('li').eq(1).text()
    ib = doc('div#content-tab--2').children().filter('ul').children().filter('li').eq(2).text()
    return (alvl + "; " + hghr + "; " + ib)

#cambridge details
def cam_get_name(course_page):
    doc = pq(course_page)
    name = doc('title')[0].text[:doc('title')[0].text.find('|') - 1]
    return name
def cam_get_description(course_page):
    doc = pq(course_page)
    return "placeholder description"
def cam_get_requirements(course_page):
    doc = pq(course_page)
    temptext = doc('fieldset.collapsible.collapsed.group-entry-requirements').find('p').eq(0).text()
    alevel = temptext[:temptext.find('\n')]
    ib = temptext[(temptext.find('\n') + 2):]
    return (alevel + '; ' + ib)

# gets the content of the page which the URL points to
def get_page(url):
    response = requests.get(url)
    page = response.content
    return page

# the page where the oxford course listing is
ox_page_url = "https://www.ox.ac.uk/admissions/undergraduate/courses/course-listing?wssl=1"
cam_page_url = "https://www.undergraduate.study.cam.ac.uk/courses"

# some strings
ox_list_section_b = "page-content-container main-content"
ox_course_marker = "//www.ox.ac.uk/admissions/undergraduate/courses-listing/"
ox_list_section_e = "webform-client-form-32032"
cam_page_prefix = "https://www.undergraduate.study.cam.ac.uk"

# main loop
if (__name__ == '__main__'):

    ox_course_list = get_ox_course_list()
    cam_course_list = get_cam_course_list()
    
    f = open('courses_data.csv', 'w')
    f.write(course_info_to_line(("university","course","description","requirements")))
    for x in ox_course_list:
        f.write(course_info_to_line(ox_get_course_info(x)))
    for x in cam_course_list:
        f.write(course_info_to_line(cam_get_course_info(x)))
