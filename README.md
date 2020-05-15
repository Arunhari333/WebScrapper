A program to scrape meetup.com to obtain details of events.

I hadn't done webscraping before and had to experiment quite a bit at the beginning. I used BeautifulSoup to scrape the response from the search url.

Steps taken:

Created a response variable with complete information of the website search url.
Cleaned the data by scraping off unwanted parts in 2 stages to obtain just the search result list data. 
Scraped the list to obtain events with the word 'React' in the title as the website search is not accurate and also shows the events with the word 'react' in the description (not case-sensitive).
Scrapped off the events with less than 500 members. Scrapped the Title, Link, Description, Date & Time, Cost, Location from the remaining data. 
Stored the scrapped data in a csv file.
