#!/usr/bin/env python

import falcon
from wsgiref import simple_server
from falcon_auth import FalconAuthMiddleware
from falcon_auth_ldap import LDAPAuthBackend

class HelloWorld:
    def on_get(self, req, resp):
        print("Received request for hello_world")
        resp.content_type = falcon.MEDIA_JSON
        resp.media = {'message': "Hello, World!"}
        resp.status = falcon.HTTP_200

ldap_conf = {
    'host': 'ldap://ldap.forumsys.com',
    'bind_dn': 'cn=read-only-admin,dc=example,dc=com',
    'bind_password': 'password',
    'base_dn': 'dc=example,dc=com',
    'user_filter': '(uid=%s)',
    'attributes': [],
}

ldap_backend = LDAPAuthBackend(**ldap_conf)
handler = falcon. API(middleware=[FalconAuthMiddleware(ldap_backend)])
handler.add_route('/hello', HelloWorld())

# Serve
print("Starting REST API")
httpd = simple_server.make_server('0.0.0.0', 8080, handler)
httpd.serve_forever()
