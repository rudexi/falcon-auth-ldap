# Falcon LDAP auth middleware

A LDAP authentication backend for falcon.

This is meant to be used with `vertexcover-io/falcon-auth`'s `FalconAuthMiddleware`,
and requires it to reuse the `BasicAuthBackend`.

# Requirements

`falcon-auth-ldap` required Python 3.6 minimum (it uses some of Python 3.6 features).

# Installation

WIP

# Usage
```python
ldap_conf = {
    'host': 'ldaps://ldap.example.com',
    'bind_dn': 'cn=mybinduser,ou=users,dc=example,dc=com',
    'bind_password': 'mysecret',
    'base_dn': 'dc=example,dc=com',
    'user_filter': '(sAMAccountName=%s)',
    'attributes': [],
}
handler = falcon.API(middleware=[FalconAuthMiddleware(LDAPAuthBackend(**ldap_conf)))
```

See [examples ](./examples/)} for more detailed example.

# Manual testing

Using the public LDAP server in `examples/hello_world.py`:
```
$curl localhost:8080/hello -u gauss:password
{"message": "Hello, World!"}
```

You can modify the `ldap_conf` to fit the LDAP server you want to
test against.
