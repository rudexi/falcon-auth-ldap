'''Simple LDAP authentication backend for Falcon'''

from falcon.errors import HTTPUnauthorized, HTTPInternalServerError

from ldap3 import Server, Connection, ALL, SUBTREE
from ldap3.core.exceptions import LDAPOperationResult, LDAPExceptionError

from falcon_auth import BasicAuthBackend

class LDAPUser:
    def __init__(self, name, dn, attributes={}):
        self.name = name
        self.dn = dn
        self.attributes = attributes

class LDAPAuthBackend(BasicAuthBackend):
    '''
    Implement an LDAP backend.

    Args:

    host(string, required):
        URL of the LDAP server
    bind_dn(string, required):
        DN of the user to search other users with
    bind_password(string, required):
        Password of the user to search other users with
    base_dn(string, required):
        Base DN to search users
    user_filter(string, required):
        A LDAP search to search the user with. %s will be replaced with the username
    attributes(string, optional):
        Attributes to retrieve from LDAP
    auth_header_prefix(string, optional):
    '''

    def __init__(self, host, bind_dn, bind_password, base_dn, user_filter, attributes=[],
        auth_header_prefix='Basic'):

        try:
            # Set variables
            self.base_dn = base_dn
            self.user_filter = user_filter
            self.attributes = attributes
            self.auth_header_prefix = auth_header_prefix
            self.bind_dn = bind_dn
            self.bind_password = bind_password
            self.server = Server(host, get_info=ALL)

            # Test LDAP bind

            bind_con = Connection(
                self.server,
                user=bind_dn,
                password=bind_password,
                raise_exceptions=True
            )
            if not bind_con.bind():
                raise Exception(f"Cannot BIND to LDAP server: {host}")
        except Exception as err:
            raise err

    def _search_user(self, username):
        try:
            bind_con = Connection(
                self.server,
                user=self.bind_dn,
                password=self.bind_password,
                raise_exceptions=True
            )
            bind_con.bind()
            user_filter = self.user_filter.replace('%s', username)
            bind_con.search(
                search_base = self.base_dn,
                search_filter = user_filter,
                attributes = self.attributes,
                search_scope = SUBTREE
            )
            response = bind_con.response
            if (
                bind_con.result['result'] == 0
                and len(response) > 0
                and 'dn' in response[0].keys()
            ):
                user_dn = response[0]['dn']
                attributes = response[0]['attributes']
                return LDAPUser(username, user_dn, attributes)
            else:
                # Could not find user in search
                raise HTTPUnauthorized(description=f"Error in search: Could not find user {username} in LDAP search")
        except LDAPOperationResult as err:
            raise HTTPUnauthorized(description=f"Error during search: {err}")
        except LDAPExceptionError as err:
            raise HTTPInternalServerError(description=f"Error during search: {err}")

    def _bind_user(self, user_dn, password):
        try:
            user_con = Connection(
                self.server,
                user=user_dn,
                password=password,
                raise_exceptions=True
            )
            user_con.bind()
            return user_con
        except LDAPOperationResult as err:
            raise HTTPUnauthorized(description=f"Error during bind: {err}")
        except LDAPExceptionError as err:
            raise HTTPInternalServerError(description=f"Error during bind: {err}")
        finally:
            user_con.unbind()

    def authenticate(self, req, resp, resource):
        username, password = self._extract_credentials(req)
        user = self._search_user(username)
        user_con = self._bind_user(user.dn, password)
        if user_con.result['result'] == 0:
            return user
        else:
            raise HTTPUnauthorized(description="")
