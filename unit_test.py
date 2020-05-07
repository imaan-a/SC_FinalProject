import unittest
from final_IA import MovieInfo 

class TestMovieInfo(unittest.TestCase):
    def setUp(self):
        self.movie1 = MovieInfo('Inception')
        self.movie2 = MovieInfo('Enfdspefse')
    
    def TestMovieInitialization(self):
        '''
        Tests that movie initialized by the imdb API is the same as expected. 
        The ID given by the program should match the expected ID. 
        '''
        self.assertEqual(self.movie1.id, 'tt1375666') 
        
    def TestNoMovieResults(self):
        '''Not valid movie input, should not show results in the API output'''
        
        self.assertIsNotIn('results', self.movie2.fulldict) 
        
    def TestGettingInfo(self):
        '''Does the get_info function get the correct info'''
        
        self.assertEqual(self.movie1.direct, 'Christopher Nolan')

    def TestRecommendations(self):
        '''Test gives list'''
        
        self.assertIsInstance(self.movie1.recommendations(), list)

if __name__ == '__main__':
    unittest.main()
    