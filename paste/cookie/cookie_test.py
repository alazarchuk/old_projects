#!/usr/bin/env python

import base64
import time
import hmac

try:
    from hashlib import sha1
except ImportError:
    # NOTE: We have to use the callable with hashlib (hashlib.sha1),
    # otherwise hmac only accepts the sha module object itself
    import sha as sha1

from paste.httpserver import serve
from paste.fileapp import DataApp, FileApp
from paste.httpexceptions import *
from paste.evalexception.middleware import EvalException
from paste.urlmap import URLMap

from paste.auth import cookie as cookie_m
from paste.auth.digest import digest_password, AuthDigestHandler
from paste.wsgilib import parse_querystring

my_realm = 'Corpus Auth'
def authfunc(environ, realm, username):
    return digest_password(realm, username, username)

class MyAuthCookieSigner(cookie_m.AuthCookieSigner):
    def sign(self, content):
        """
        Sign the content returning a valid cookie (that does not
        need to be escaped and quoted).  The expiration of this
        cookie is handled server-side in the auth() function.
        """
        cookie = base64.encodestring(
            hmac.new(self.secret, content, sha1).digest() +
            cookie_m.make_time(time.time() + 60*self.timeout) +
            content)[:-1]
        cookie = cookie.replace("/", "_").replace("=", "~").replace("\n", "")

        if len(cookie) > self.maxlen:
            raise cookie_m.CookieTooLarge(content, cookie)
        return cookie

    def auth(self, cookie):
        """
        Authenticate the cooke using the signature, verify that it
        has not expired; and return the cookie's content
        """
        decode = base64.decodestring(
            cookie.replace("_", "/").replace("~", "="))
        signature = decode[:cookie_m._signature_size]
        expires = decode[cookie_m._signature_size:cookie_m._header_size]
        content = decode[cookie_m._header_size:]
        if signature == hmac.new(self.secret, content, sha1).digest():
            if int(expires) > int(cookie_m.make_time(time.time())):
                return content
            else:
                # This is the normal case of an expired cookie; just
                # don't bother doing anything here.
                pass
        else:
            # This case can happen if the server is restarted with a
            # different secret; or if the user's IP address changed
            # due to a proxy.  However, it could also be a break-in
            # attempt -- so should it be reported?
            pass


cookie_m.AuthCookieHandler.signer_class = MyAuthCookieSigner

def get_info(environ, start_response):
#    command = dict(parse_querystring(environ)).get('command','')
    page = str(parse_querystring(environ))

#    if command == 'clear':
#        if 'REMOTE_USER' in environ:
#            del environ['REMOTE_USER']
#        if 'REMOTE_SESSION' in environ:
#            del environ['REMOTE_SESSION']
#    else:
#        environ['REMOTE_SESSION'] = authfunc(environ, my_realm, environ['REMOTE_USER'] )

#    if environ.get('REMOTE_USER'):
#        page = '<html><body>Welcome %s (%s)</body></html>'
#        page %= (environ['REMOTE_USER'], environ['REMOTE_SESSION'])
#    else:
#        page = ('<html><body><form><input name="user" />'
#                '<input type="submit" /></form></body></html>')
    return DataApp(page, content_type="text/plain")(
                   environ, start_response)

root_app = URLMap()
root_app['/get_info'] = get_info


serve(EvalException(
        cookie_m.AuthCookieHandler(
                AuthDigestHandler(root_app, my_realm, authfunc),
                secret="TEST2", timeout=60)),
      host='0.0.0.0', port=8041)

