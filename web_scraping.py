import requests
from bs4 import BeautifulSoup
from csv import writer

keyword = 'React'
response = requests.get('https://www.meetup.com/find/events/?allMeetups=false&keywords=React&radius=25&userFreeform=New+York%2C+New+York%2C+USA&mcId=c10001&mcName=New+York%2C+NY')

soup = BeautifulSoup(response.text, 'html.parser')

scrape = soup.select('.row-item .chunk')
posts = []
for post in scrape:
    if len(post.select('.text--labelSecondary')) != 0:
        posts.append(post)
events = []
for post in posts:
    event = post.find_all('span')[1].get_text().replace('\n', '')
    if event.find('React') != -1:
        events.append(post)
# print(events)

events500 = []
for event in events:
    linkTemp = event.find_all(class_='text--labelSecondary')[0].find('a')['href']
    res = requests.get(linkTemp)
    temp = BeautifulSoup(res.text, 'html.parser')
    members = temp.find(class_='groupHomeHeaderInfo-memberLink').get_text()
    membersSplit = members.split(' ')
    membersStr = membersSplit[0].replace(',', '')
    membersNum = int(membersStr)
    if membersNum > 500:
        events500.append(event)

with open('posts.csv', 'w') as csv_file:
    csv_writer = writer(csv_file)
    headers = ['Title', 'Link', 'Description', 'Date & Time', 'Cost', 'Location']
    csv_writer.writerow(headers)

    for event in events500:
        link = event.find_all(class_='text--labelSecondary')[0].find('a')['href']
        linkTemp = event.find(class_='event')['href']
        res = requests.get(linkTemp)
        temp = BeautifulSoup(res.text, 'html.parser')

        title = temp.find(class_='pageHead-headline text--pageTitle').get_text()
        description = temp.find(class_='event-description runningText').get_text()
        date_time_comp = temp.find(class_='eventTimeDisplay-startDate')
        date_time = ''
        for child in date_time_comp.children:
            date_time = date_time + ' ' + child.get_text()
        date_time_comp1 = date_time_comp.find_next_sibling()
        for child in date_time_comp1.descendants:
            c = str(child)
            if c[0] != '<' and c != ' ':
                date_time = date_time + ' ' + c.strip()
        cost = temp.find(attrs={'data-e2e': 'event-footer--price-label'}).contents[0].get_text()
        location = temp.find('address').contents[0].get_text()
        csv_writer.writerow([title, link, description, date_time, cost, location])


