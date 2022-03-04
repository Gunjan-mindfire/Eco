from django.core.mail import EmailMessage
import re
from EcoMail import settings

from django.core.mail import send_mail
from django.core.mail import EmailMultiAlternatives
from .models import scrapData

import requests
from bs4 import BeautifulSoup
from celery import shared_task



@shared_task(bind=True)
def scrapnews(self,args):
    new_list_of_news = scrapData.objects.all()[:4]
    list_of_news_content = ""
    for news in new_list_of_news:
        link = "https://economictimes.indiatimes.com"+news.link
        list_of_news_content = list_of_news_content + "<tr style='text-align:center'><td style='border:solid 1px;'><a href="+link+">"+news.title+"</a></td></tr>"
    subject = "Scrapped Data"
    message = "<html><body>   <br> <H1>Lastest Economic News from Economic Times </H1><br>   <table style='width:100%;padding-right: 10%;font-size: 25px;'><tbody><tr style='text-align:center; background:#753436;color:#aa934f;' >"+list_of_news_content+"</tbody>   </table>   </body>   </html>"
    receiver = [args]
    reportmail = EmailMultiAlternatives(subject,message, settings.EMAIL_HOST_USER,receiver)
    reportmail.content_subtype = "html"
    reportmail.send()
    return "Mail sent"

@shared_task(bind=True)
def scrap(self):
    url = 'https://economictimes.indiatimes.com/'
    reqs = requests.get(url)
    soup = BeautifulSoup(reqs.text, 'lxml')
    last_5_records = scrapData.objects.values_list(flat=True).order_by('-id')[:5]
    remove_excluding5 = scrapData.objects.exclude(pk__in = list(last_5_records)).delete()
    for li in soup.find('ul', {'class': 'newsList'}).findAll('li')[:5]:
        if li.a.get('href')!=None:
            s = scrapData()
            s.link = li.a.get('href')
            s.title = li.a.text
            s.save()

    return "Scraped 5 news"





