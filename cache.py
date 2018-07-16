import json
from util import Util

class Cache:

    CACHE_HIT = 1
    CACHE_MISS = 0
    CONNECTION_PROTOCOL = ''
    cache_directory = {}

    def __init__(self, protocol):
        self.CONNECTION_PROTOCOL = protocol
        self.load_cache_directory()

    def lookup(self, request):
        '''
            Search directory for occurrences
        '''
        lookup_result = Util.lookup_in_dict(request, self.cache_directory)

        if (lookup_result == self.CACHE_HIT):
            return (self.CACHE_HIT, self.instant_service(request))

        else:
            return (self.CACHE_MISS, 0)
            
    def store(self, request, data):
        '''
            Save request and data to cache
        '''
        cached_data = {
            request: data
        }

        # Append to cache dictionary
        self.cache_directory = {**self.cache_directory, **cached_data}

        # Append to cache json
        cache_file = self.CONNECTION_PROTOCOL + '_cache.json'
        with open(cache_file, 'w') as cache_directory:
            json.dump(self.cache_directory, cache_directory)

    def instant_service(self, request):
        '''
            Serve the request
        '''
        requested_data = self.cache_directory[request]
        return requested_data

    def load_cache_directory(self):
        cache_file = self.CONNECTION_PROTOCOL + '_cache.json'

        with open(cache_file) as handle:
            self.cache_directory = json.loads(handle.read())