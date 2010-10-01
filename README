This is an unofficial third-party Python wrapper for the `Agent Storm Web Services API`_. `Agent Storm`_ is a property management system/IDX provider for real estate agents.

.. _Agent Storm Web Services API: http://support.agentstorm.com/faqs/api/api-documentation
.. _Agent Storm: http://www.agentstorm.com

Example Usage::

    >>> from agentstorm.wrapper import AgentStorm
    >>> c = AgentStorm('mysubdomain', 'MY_API_KEY')
    >>> properties = c.properties.all()
    >>> properties.Count
    5
    
    >>> resp = c.properties.filter(ListPrice__gt=200000)
    >>> for i in resp.Properties:
        print i.Id, i.FullAddress, i.City, i.State
    106023 83 Fox Hill Buffalo Grove IL
    106025 120 Main St. Evenston IL
    106027 625 Michigan Ave. Chicago IL
    106024 1250 Armitage Ave Chicago IL        
    
    >>> prop = c.properties.get(106023)
    >>> prop.FullAddress
    83 Fox Hill
    
    >>> resp = c.properties.filter(
            ListPrice__range=(300000, 400000), 
            Zip=60089, 
            sort="ListPrice", 
            sort_direction="DESC")
    >>> import locale
    >>> locale.setlocale(locale.LC_ALL, '')
    >>> for i in resp.Properties:
    >>>     print "A property at %s in %s, %s for %s" % \
                (i.FullAddress, i.City, i.State, locale.currency(int(i.ListPrice), grouping=True))
    A property at 83 Fox Hill in Buffalo Grove, IL for $380,000.00    
    
    >>> resp = c.companies.all()
    >>> for i in resp.Companies:
    >>>     print "%s (%s)" % (i.Name, i.Industry.Name)
    My Test Company (Accident & Health Insurance)    