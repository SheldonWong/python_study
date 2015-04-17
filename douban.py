#!/usr/bin/env python
# -*- encoding: utf-8 -*-
# vim: set et sw=4 ts=4 sts=4 ff=unix fenc=utf8:
# Created on 2014-09-10 12:05:42
 
import os
import re
import json
import datetime
from libs.pprint import pprint
from libs.base_handler import *
 
class Handler(BaseHandler):
    '''
    this is a sample handler
    '''
    def on_start(self):
        self.crawl('http://www.douban.com/location/china/', callback=self.location_page)
            
    @config(age=60)
    def location_page(self, response):
        if response.doc('HTML>BODY>DIV#wrapper>DIV#content>DIV.grid-free.clearfix>DIV.article>DIV#db-events-list>UL.events-list>LI.list-entry>DIV.info>DIV.title>A'):
            return self.index_page(response)
        
        for each in response.doc('DIV.location>A').items():
            if 'douban.com/location/' in each.attr.href:
                city = each.attr.href.split('/')[-2]
            else:
                city = each.attr.href.split('.')[0][7:]
            self.crawl('http://www.douban.com/location/%s/events/week-all' % city,
                       callback=self.location_page)
        
 
    @config(age=24*60*60)
    def index_page(self, response):
        for each in response.doc('HTML>BODY>DIV#wrapper>DIV#content>DIV.grid-free.clearfix>DIV.article>DIV#db-events-list>UL.events-list>LI.list-entry>DIV.info>DIV.title>A').items():
            self.crawl(each.attr.href, callback=self.detail_page)
            
        for each in response.doc('HTML>BODY>DIV#wrapper>DIV#content>DIV.grid-free.clearfix>DIV.article>DIV#db-events-list>DIV.paginator>A').items():
            self.crawl(each.attr.href, callback=self.index_page)
    
    @config(age=24*60*60)
    def detail_page(self, response):
        return {
            "url": response.url,
            "title": response.doc('HTML>BODY>DIV#wrapper>DIV#content DIV.article DIV#event-info>DIV.event-info>H1').text(),
            "place": response.doc("HTML>BODY>DIV#wrapper>DIV#content DIV.article DIV#event-info>DIV.event-info>DIV.event-detail>SPAN.micro-address").text(),
            "time": [x.text() for x in response.doc("DIV.article>DIV.related_info DIV.buy-tickets-bd-con>DIV.buy-tickets-bd>DIV.buy-tickets-item>DIV.buy-tickets-itemcon.tickets-con-stage").items()] or [response.doc("DIV.article>DIV.eventwrap>DIV#event-info>DIV.event-info>DIV.event-detail>UL.calendar-strs>LI.calendar-str-item").text()] if response.doc("DIV.article>DIV.eventwrap>DIV#event-info>DIV.event-info>DIV.event-detail>UL.calendar-strs>LI.calendar-str-item") else [],
            "price": [x.text() for x in response.doc("DIV.buy-tickets-bd-con>DIV.buy-tickets-bd>DIV.buy-tickets-item>DIV.tickets-con-price>A.buy-tickets-info").items()] or [response.doc(u'DIV.article DIV#event-info>DIV.event-info>DIV.event-detail>SPAN.pl:contains("费用")')[0].tail.strip()] if response.doc(u'DIV.article DIV#event-info>DIV.event-info>DIV.event-detail>SPAN.pl:contains("费用")') else [],
            "mcid": response.doc(u'DIV.article DIV#event-info>DIV.event-info>DIV.event-detail>SPAN.pl:contains("类型") ~ a').text(),
            "city": response.doc('DIV.nav-primary>DIV.local-label>A.label').text(),
        }