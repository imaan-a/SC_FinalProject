#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon May  4 14:59:14 2020

@author: imaanamlani
"""

import requests
import json

class MovieInfo:

    def __init__(self, movie):
        
        self.imdb_host = 'imdb8.p.rapidapi.com'
        self.rapidapi_key = '2f253b2b1fmshf52ace529d3e4fdp100abfjsnc5a369008482'
        self.movie = movie  
        #assert len(self.movie) >= 2, 'Enter more characters to search' 
        
        url = 'https://imdb8.p.rapidapi.com/title/find'
        querystring = {"q":self.movie}
        self.imdbheaders = {'x-rapidapi-host': self.imdb_host,
                   'x-rapidapi-key': self.rapidapi_key}
        response = requests.request('GET', url, headers=self.imdbheaders, 
                                    params=querystring)
        fulldict = json.loads(response.text)
        
        if 'results' in fulldict:
            results = fulldict['results']
        else:
            raise Exception ('No Results Found')
            
        self.first_result = results[0]
        self.id = self.first_result['id'][7:-1]
        
        
    def get_info(self):   
        
        title = self.first_result['title']
        year = self.first_result['year']
        kind = self.first_result['titleType'].capitalize()
        cast1 = self.first_result['principals'][0]['name']
        cast2 = self.first_result['principals'][1]['name']
        cast3 = self.first_result['principals'][2]['name']
        #add error handling (not three cast, no principles, etc)
        run = self.first_result['runningTimeInMinutes']
        
        crewrl = "https://imdb8.p.rapidapi.com/title/get-top-crew"
        crewq = {"tconst": self.id}
        crew_res = requests.request("GET", crewrl, headers=self.imdbheaders, params=crewq)
        crewdict = json.loads(crew_res.text)
        direct = crewdict['directors'][0]['name']
        
        out1 = '%s (%d) - %s \n Run Time: %d mins\n'\
                'Director: %s'%(title, year, kind, run, direct) 
        out2 = ['Principle Cast:', cast1, cast2, cast3]
        
        return out1, out2
    
    def get_pic_details(self):
        
        pic_url = self.first_result['image']['url']
        
        return pic_url
    
    def recommendations(self):
        
        r_url = "https://imdb8.p.rapidapi.com/title/get-more-like-this"
        r_query = {"currentCountry":"US","purchaseCountry":"US","tconst":self.id}
        dets_url = "https://imdb8.p.rapidapi.com/title/get-overview-details"

        recresponse = requests.request("GET", r_url, headers=self.imdbheaders, params=r_query)
        recdict = json.loads(recresponse.text)
        if len(recdict) == 0:
            raise Exception ('No similar titles found')
        elif len(recdict) < 5:
            rec_num = len(recdict)
        else: 
            rec_num = 5
        
        recs = []
        for i in range(rec_num):
            rec_id = recdict[i][7:-1]
            dets_query = {"currentCountry":"US","tconst":rec_id}
            dets_res = requests.request("GET", dets_url, headers=self.imdbheaders, params=dets_query)
            detdict = json.loads(dets_res.text)
            title = detdict['title']['title']
            recs.append(title)
        
        recs.insert(0, 'You Might Also Like:')
        
        return recs
    
    def wheretowatch(self, country):
        
        utel_url = 'https://utelly-tv-shows-and-movies-availability-v1.p.rapidapi.com/lookup'
        c_dict = {'United States':'us', 'Canada': 'ca', 'United Kingdom':'uk',
                  'Austrailia':'au', 'Spain':'es', 'France':'fr', 'Brazil':'br',
                  'Hong Kong':'hk', 'Japan':'jp'}
        utel_query = {"term":self.movie,"country": c_dict[country]}
        utelly_host = 'utelly-tv-shows-and-movies-availability-v1.p.rapidapi.com'
        utelheaders = {'x-rapidapi-host': utelly_host, 'x-rapidapi-key': self.rapidapi_key}
        
        avail_res = requests.request("GET", utel_url, headers=utelheaders, params=utel_query)
        availdict = json.loads(avail_res.text)
        locations = availdict['results'][0]['locations']
        services = []
        links = []
        for i in range(len(locations)):
            service = locations[i]['display_name'] 
            link = locations[i]['url']
            services.append(service)
            links.append(link)
        if len(services) == 0:
            raise Exception('Cannot find title availability')
        
        return services, links
        
if __name__ == '__main__':
    jw = MovieInfo('John Wick')
    place = jw.wheretowatch('us')
    print(place)
    