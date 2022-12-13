import requests


def get_payload(page_num: int) -> dict:
    method = 'GET'
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) '
                             'Chrome/67.0.3396.79 Safari/537.36'}
    url = f'https://reqres.in/api/users?page={page_num}'
    response = requests.request(method, url, headers=headers)
    assert response.status_code == 200, f'Request failed with status code: {response.status_code}'
    return response.json()


def get_user_full_name_list(first_id: int, last_id: int) -> list:
    result = []

    if not isinstance(first_id, int) or not isinstance(last_id, int):
        return result

    if first_id > last_id:
        first_id, last_id = last_id, first_id

    if first_id < 1 or last_id > 12:
        return result

    page_num = 1
    payload = get_payload(page_num)

    data = payload['data']

    if last_id > payload['per_page']:
        page_num = 2
        data += get_payload(page_num)['data']

    result = sorted([' '.join((record['first_name'], record['last_name'])) for record in data
                     if first_id <= record['id'] <= last_id])

    return result


assert get_user_full_name_list(1, 12) == ['Byron Fields', 'Charles Morris', 'Emma Wong', 'Eve Holt', 'George Bluth',
                                          'George Edwards', 'Janet Weaver', 'Lindsay Ferguson', 'Michael Lawson',
                                          'Rachel Howell', 'Tobias Funke', 'Tracey Ramos']
assert get_user_full_name_list(6, 7) == ['Michael Lawson', 'Tracey Ramos']
assert get_user_full_name_list(3, 9) == ['Charles Morris', 'Emma Wong', 'Eve Holt', 'Lindsay Ferguson',
                                         'Michael Lawson', 'Tobias Funke', 'Tracey Ramos']
assert get_user_full_name_list(9, 3) == ['Charles Morris', 'Emma Wong', 'Eve Holt', 'Lindsay Ferguson',
                                         'Michael Lawson', 'Tobias Funke', 'Tracey Ramos']
assert get_user_full_name_list(3, 3) == ['Emma Wong']
assert get_user_full_name_list(0, 12) == []
assert get_user_full_name_list(1, 13) == []
assert get_user_full_name_list(-3, 9) == []
assert get_user_full_name_list(3, -9) == []
assert get_user_full_name_list('3', 9) == []
assert get_user_full_name_list(3, '9') == []
