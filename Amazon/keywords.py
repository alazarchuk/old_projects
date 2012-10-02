import SOAPpy

url = 'http://soap.amazon.com/schemas3/AmazonWebServices.wsdl'
proxy = SOAPpy.WSDL.Proxy(url)

# show methods retrieved from WSDL
print '%d methods in WSDL:' % len(proxy.methods) + '\n'
for key in proxy.methods.keys():
    print key
print

# search request
_query = 'spotted owl'
request = { 'keyword':  _query, 
            'page':     '1', 
            'mode':     'books', 
            'tag':      '', 
            'type':     'lite',
            'devtag':   '0J356Z09CN88KB743582' }

results = proxy.KeywordSearchRequest(request)

# display results
print 'Amazon.com search for  " ' + _query + ' "\n'
print 'total pages of results (max 10 per page): ' + str(results.TotalPages)
print 'total results: ' + str(results.TotalResults) + '\n'

# only show first result here
if (results.TotalResults > 0):
    print 'displaying first result (of %s):\n' %results.TotalResults
    details = results.Details[0]
    
    # we must use the _keys() method of SOAPpy Types.py for arrayType
    for key in details._keys():
        print key + ': ' + details[key]
    print
