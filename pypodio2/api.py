# -*- coding: utf-8 -*-
from . import transport, client


def build_headers(authorization_headers, user_agent):
    headers = transport.KeepAliveHeaders(authorization_headers)
    if user_agent is not None:
        headers = transport.UserAgentHeaders(headers, user_agent)
    return headers


def OAuthClient(api_key, api_secret, login, password, user_agent=None,
                domain="https://api.podio.com"):
    auth = transport.OAuthAuthorization(login, password,
                                        api_key, api_secret, domain)
    return AuthorizingClient(domain, auth, user_agent=user_agent)


def OAuthRefreshTokenClient(client_id, client_secret, refresh_token, user_agent=None,
                            domain="https://api.podio.com"):
    auth = transport.OAuthRefreshTokenAuthorization(client_id, client_secret,
                                                    refresh_token, domain)
    return AuthorizingClient(domain, auth, user_agent=user_agent)


def OAuthFromExistingTokens(tokens, user_agent=None, domain="https://api.podio.com"):
    auth = transport.OAuthAuthorizationFromTokens(tokens)
    return AuthorizingClient(domain, auth, user_agent=user_agent)


def OAuthAppClient(client_id, client_secret, app_id, app_token, user_agent=None,
                   domain="https://api.podio.com"):
    auth = transport.OAuthAppAuthorization(app_id, app_token,
                                           client_id, client_secret, domain)

    return AuthorizingClient(domain, auth, user_agent=user_agent, app_id=app_id)


def AuthorizingClient(domain, auth, user_agent=None, app_id=None):
    """Creates a Podio client using an auth object."""
    http_transport = transport.HttpTransport(domain, build_headers(auth, user_agent))
    client_ = client.Client(http_transport)
    client_.app_id = app_id
    return client_, auth
