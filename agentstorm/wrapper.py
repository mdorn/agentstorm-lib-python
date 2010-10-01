from urllib import urlencode
from urllib2 import urlopen
try:
    import json # Python 2.6
except:
    try:
        import simplejson as json # < 2.6 may have simplejson installed
    except:
        sys.exit('No json module found')

from utils import ObjFromDict

class AgentStormException(Exception):
    pass

class AgentStorm(object):
    '''
    Main API wrapper class
    '''
    def __init__(self, subdomain, api_key):
        self.subdomain = subdomain
        self.api_key = api_key
        self.uri = 'http://%s.agentstorm.com/' % (subdomain)
        self.properties = self.Property(self) # is passing self like this kosher? may need better OO-fu
        self.properties.cities = self.City(self)
        self.properties.tags = self.Resource('properties/tags', self)
        self.contacts = self.Resource('contacts', self)
        self.companies = self.Resource('companies', self)
        self.file = None
        
    def _connect(self, resource, id=None, query=None):
        '''
        Constructs the URI and makes the request: only to be used by Resource methods
        '''
        if self.file:
            data = json.load(self.file)
        else:
            if id:
                resource = '%s/%s.json' % (resource, id)
            else:
                resource = resource + '.json'
            params={}
            params['apikey'] = self.api_key
            if query:
                params.update(query)
            query_string = urlencode(params)
            endpoint = '%s%s?%s' % (self.uri, resource, query_string)
            response = urlopen(endpoint)
            data = json.load(response)
        
        if data.has_key('Errors'):
            data = ObjFromDict(data)
            raise AgentStormException('Error %s: %s' % (data.Errors.Error.Code, data.Errors.Error.Description))
        else:
            return ObjFromDict(data)
    
    class Resource(object):
        '''
        Base class for AgentStorm resources like property, company, or contact
        '''

        def __init__(self, name, inst):
            self.name = name
            self.inst = inst

        def all(self, **kwargs):
            query = {}
            for i in kwargs:
                if i not in ['offset', 'limit', 'sort', 'sort_direction']:
                    raise AgentStormException('Error: %s is an invalid argument for all().  Did you mean to use filter()?' % i)
                else:
                    query[i] = kwargs[i]
            return self.inst._connect(self.name, query=query)

        def get(self, id):
            item = self.inst._connect(self.name, str(id))
            item = getattr(item, self.name.title())[0]
            return item
            
        def filter(self, **kwargs):
            query = {}
            for i in kwargs:
                compare = i.split('__')
                if len(compare) > 1:
                    field = compare[0]
                    oper = compare[1]
                    if oper == 'lt':
                        query[field] = str(kwargs[i]) + '-'
                    elif oper == 'gt':
                        query[field] = str(kwargs[i]) + '+'
                    elif oper == 'range':
                        query[field] = '%s:%s' % (kwargs[i][0], kwargs[i][1])
                else:
                    query[i] = kwargs[i]
            items = self.inst._connect(self.name, query=query)
            return items
            
    class Property(Resource):
        
        def __init__(self, inst):
            self.name = 'properties'
            self.inst = inst        
        
        def get_by_tag(self, tag):
            items = self.inst._connect('properties/tags', tag)
            
    class City(Resource):
        
        def __init__(self, inst):
            self.name = 'properties/cities'
            self.inst = inst        
        
        def get_by_tag(self, tag):
            items = self.inst._connect('properties/tags/%s/cities' % tag)
