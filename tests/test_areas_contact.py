from tests.utils import check_client_method


def test_get_contacts():
    client, check_assertions = check_client_method()
    result = client.Contact.get_contacts()
    check_assertions(result, 'GET', '/contact/')

    client, check_assertions = check_client_method()
    result = client.Contact.get_contacts(limit=100)
    check_assertions(result, 'GET', '/contact/?limit=100')
