# -*- coding: utf-8 -*-

import pycurl
import StringIO
import lxml.html

################################################################################
################################################################################
################################################################################
### 
###
### Прокся может быть HTTP, SOCKS4, SOCKS5. При использовании прокси, при    
### создании контруктора надо передаватьего списком из нескольких значений:   
### proxy = ['HTTP', 'ip', 'port', 'login', 'password'], в случае если прокся 
### анонимная, поля login и password дожны быть None. Все поля обязательны к 
### заполнению. Работоспособность с проксей не проверял.
###
################################################################################
################################################################################
################################################################################

class vk_bot():
    def __init__(self, email, password, myid, proxy):
        # Первоначальные данные начального объекта
        self.email = email
        self.password = password
        self.myid = myid
        self.proxy = proxy 
        
        # Пустая куки изначально.
        self.cookie = ''
        # Создание объекта curl'a
        self.curlobj = pycurl.Curl()
        
# --- Авторизация вконтакте  ----        
    def login(self):
        self.curlobj.setopt(pycurl.URL, 'http://vk.com/login.php?email='+email+'&pass='+password)
        self.curlobj.setopt(pycurl.HTTPHEADER, ["Accept:"])
        self.output = StringIO.StringIO() # Выходящий поток. Значение == код страницы.
        self.curlobj.setopt(pycurl.WRITEFUNCTION, self.output.write) # Пишем в поток.
        
        if self.proxy is None:
            print 'No use proxy!'
        else:
            if self.proxy[0] == 'HTTP':
                self.curlobj.setopt(pycurl.PROXYTYPE, pycurl.PROXYTYPE_HTTP)
            elif self.proxy[0] == 'SOCKS4':
                self.curlobj.setopt(pycurl.PROXYTYPE, pycurl.PROXYTYPE_SOCKS4)
            elif self.proxy[0] == 'SOCKS5':
                self.curlobj.setopt(pycurl.PROXYTYPE, pycurl.PROXYTYPE_SOCKS5)
            if self.proxy[3] is not None:
                self.curlobj.setopt(pycurl.PROXY, '%s:%s' % self.proxy[1], self.proxy[2])
                self.curlobj.setopt(pycurl.PROXYUSERPWD, '%s:%s' % self.proxy[3], self.proxy[4])
            else:
                self.curlobj.setopt(pycurl.PROXY, '%s:%s' % self.proxy[1], self.proxy[2])
        
        self.curlobj.setopt(pycurl.FOLLOWLOCATION, 1)
#        self.curlobj.setopt(pycurl.MAXREDIRS, 5) # При условии редиректов, ограничение позволит попасть на нужную страницу если она скрыта.
        self.curlobj.setopt(pycurl.COOKIEFILE, self.cookie) # cookie файл, без него не возможно получение второй и последюущих страниц, контакт считает что мы не авторизованы + ошибка SSL
        self.curlobj.perform()
        self.friends_page()
        #loginpage = self.outputgetvalue()

# --- Получение страницы друзей ---
    def friends_page(self):
        self.curlobj.setopt(pycurl.URL, 'http://m.vk.com/friends?id=105719996')
        self.curlobj.setopt(pycurl.HTTPHEADER, ["Accept:"])
        self.curlobj.setopt(pycurl.WRITEFUNCTION, self.output.write)
        self.curlobj.setopt(pycurl.FOLLOWLOCATION, 1)
        self.curlobj.setopt(pycurl.MAXREDIRS, 5)
        self.curlobj.setopt(pycurl.COOKIEFILE, self.cookie)
        self.curlobj.perform()
        friendspage = self.output.getvalue()
        allfriends = friendspage.find('</html><!DOCTYPE html>')
        self.allfriends = friendspage[allfriends:]
        self.ids()
        
    def ids(self):
        listofid = []
        doc = lxml.html.document_fromstring('%s' % self.allfriends)
        self.frofid = doc.xpath('/html/body/div/div/div[@class="friend"]/a')
        for idi in self.frofid:
            listofid.append(idi.get('href'))
        print listofid
        
        

email = '+79165709948'
password = '*'
myid = '164266801'
proxy = None

vk_bot(email, password, myid, proxy).login()
