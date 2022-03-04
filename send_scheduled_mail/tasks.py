from django.core.mail import EmailMessage
import re
from EcoMail import settings

from django.core.mail import send_mail
from django.core.mail import EmailMultiAlternatives

import requests
from bs4 import BeautifulSoup
from celery import shared_task


@shared_task(bind=True)
def scrapnews(self,args):
    url = 'https://economictimes.indiatimes.com/'
    reqs = requests.get(url)
    soup = BeautifulSoup(reqs.text, 'lxml')
    list_of_news_content = ""
    for li in soup.find('ul', {'class': 'newsList'}).findAll('li')[:4]:
        if li.a.get('href')!=None:
            link = "https://economictimes.indiatimes.com" + li.a.get('href')
            list_of_news_content = list_of_news_content + "<tr style='text-align:center'><td style='border:solid 1px;'><a href="+link+">"+li.a.text+"</a></td></tr>"

    
    subject = "Scrapped Data"
    message = "<html><body> <br> <H1>Lastest Economic News from Economic Times </H1><br>   <table style='width:100%;padding-right: 10%;font-size: 25px;'><tbody><tr style='text-align:center; background:#753436;color:#aa934f;' >"+list_of_news_content+"</tbody>   </table>   </body>   </html>"
    receiver = [args]
    reportmail = EmailMultiAlternatives(subject,message, settings.EMAIL_HOST_USER,receiver)
    reportmail.content_subtype = "html"
    reportmail.send()
    return "Scraped 5 news"



