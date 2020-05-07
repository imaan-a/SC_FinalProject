
import json
import requests


class MovieInfo:
    '''
    This class is used to extract relevant data from the Imdb and Utelly APIs.
    The data can then be used with a graphical user interface to see visual.
    '''

    def __init__(self, movie):
        '''
        Initializes the Movie Info function with a movie title and searches the
        title in the imdb API.

        **Parameters**
            movie: **str**
                Movie title or title fragment as given by user through the gui.
        '''
        self.rapidapi_key = '2f253b2b1fmshf52ace529d3e4fdp100abfjsnc5a3'\
                            '69008482'
        self.movie = movie
        self.imdb_host = 'imdb8.p.rapidapi.com'
        assert len(self.movie) >= 2, 'Enter more characters to narrow search'

        url = 'https://imdb8.p.rapidapi.com/title/find'
        querystring = {"q": self.movie}
        self.imdbheaders = {'x-rapidapi-host': self.imdb_host,
                            'x-rapidapi-key': self.rapidapi_key}
        response = requests.request('GET', url, headers=self.imdbheaders,
                                    params=querystring)
        self.fulldict = json.loads(response.text)

        if 'results' in self.fulldict:
            results = self.fulldict['results']
        else:
            raise Exception('No Results Found')

        self.first_result = results[0]
        self.id = self.first_result['id'][7:-1]

    def get_info(self):
        '''
        Extracts relevant information about initialized movie title from imdb.

        **Parameters**
            None

        **Returns**
            out1: **str**
                Formatted string with movie title, year, runtime and director
            out2: **list, str**
                List of strings with title and 3 principle cast members
        '''
        self.title = self.first_result['title']
        year = self.first_result['year']
        kind = self.first_result['titleType'].capitalize()
        cast1 = self.first_result['principals'][0]['name']

        # error handling for if there are less than 3 cast members
        try:
            cast2 = self.first_result['principals'][1]['name']
        except:
            cast2 = ''

        try:
            cast3 = self.first_result['principals'][2]['name']
        except:
            cast3 = ''

        run = self.first_result['runningTimeInMinutes']

        crewrl = "https://imdb8.p.rapidapi.com/title/get-top-crew"
        crewq = {"tconst": self.id}
        crew_res = requests.request("GET", crewrl, headers=self.imdbheaders,
                                    params=crewq)
        crewdict = json.loads(crew_res.text)
        self.direct = crewdict['directors'][0]['name']

        out1 = '%s (%d) - %s \n Run Time: %d mins\n'\
            'Director: %s' % (self.title, year, kind, run, self.direct)
        out2 = ['Principle Cast:', cast1, cast2, cast3]

        return out1, out2

    def get_plot(self):
        '''
        Gets the plot of the initialized movie title.

        **Parameters**
            None

        **Returns**
            plot: **list, str**
                The plot of the movie as a string.
        '''
        plot_url = "https://imdb8.p.rapidapi.com/title/get-plots"
        plot_query = {"tconst": self.id}
        response = requests.request("GET", plot_url, headers=self.imdbheaders,
                                    params=plot_query)
        dicty = json.loads(response.text)
        if 'plots' in dicty:
            plot = dicty['plots'][0]['text']
        else: 
            plot = 'No plot summary available'

        return plot

    def get_pic_details(self):
        '''
        Gives link to initialized movie poster.

        **Parameters**
            None

        **Returns**
            pic_url: **str**
                String of url that links to the movie poster.
        '''
        pic_url = self.first_result['image']['url']

        return pic_url

    def recommendations(self):
        '''
        Gives recommendations for other movies based on the initialized title.
        Uses an endpoint in the imdb API.

        **Parameters**
            None

        **Returns**
            recs: **list, str**
                List of titles similar to initialized movie.
        '''
        r_url = "https://imdb8.p.rapidapi.com/title/get-more-like-this"
        r_query = {"currentCountry": "US", "purchaseCountry": "US",
                   "tconst": self.id}
        dets_url = "https://imdb8.p.rapidapi.com/title/get-overview-details"

        recresponse = requests.request("GET", r_url, headers=self.imdbheaders,
                                       params=r_query)
        recdict = json.loads(recresponse.text)

        if len(recdict) == 0:
            raise Exception('No similar titles found')
        elif len(recdict) < 5:
            rec_num = len(recdict)  # if API gives less than 5 similar titles
        else:
            rec_num = 5

        recs = []
        for i in range(rec_num):
            rec_id = recdict[i][7:-1]
            dets_query = {"currentCountry": "US", "tconst": rec_id}
            dets_res = requests.request("GET", dets_url,
                                        headers=self.imdbheaders,
                                        params=dets_query)
            detdict = json.loads(dets_res.text)
            name = detdict['title']['title']
            recs.append(name)

        recs.insert(0, 'You Might Also Like:')

        return recs

    def wheretowatch(self, country):
        '''
        Uses the Utelly API to show where the titles can be found online to
        watch in nine different countries.

        **Parameters**
            country: **str**
                Country in which user wants to find streaming service.

        **Returns**
            None
        '''
        utel_url = 'https://utelly-tv-shows-and-movies-availability-v1.p.'\
            'rapidapi.com/lookup'
        c_dict = {'United States': 'us', 'Canada': 'ca',
                  'United Kingdom': 'uk', 'Austrailia': 'au', 'Spain': 'es',
                  'France': 'fr', 'Brazil': 'br', 'Hong Kong': 'hk',
                  'Japan': 'jp'}
        utel_query = {"term": self.title, "country": c_dict[country]}
        utelly_host = 'utelly-tv-shows-and-movies-availability-v1.p.'\
            'rapidapi.com'
        utelheaders = {'x-rapidapi-host': utelly_host,
                       'x-rapidapi-key': self.rapidapi_key}

        avail_res = requests.request("GET", utel_url, headers=utelheaders,
                                     params=utel_query)
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
    pass
