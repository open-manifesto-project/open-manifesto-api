import json


class ClientJSON:

    def __init__(self, app):
        self.client = app.test_client()
        self.headers = {'content-type': 'application/json'}

    def set_token(self, response):
        token = json_loads_data(response, 'access_token')
        self.headers.update({'authorization': token})

    def revoke_token(self):
        if self.headers.get('authorization'):
            self.headers.pop('authorization')

    def login(self, email='test@wadobo.com', pwd='qwerty'):
        data = {'email': email, 'pwd': pwd}
        response = self.post('/api/player/login', data)
        self.set_token(response)
        return response

    def logout(self):
        response = self.get('/api/player/logout')
        self.revoke_token()
        return response

    def get(self, url, data={}):
        return self.client.get(url, data=json.dumps(data), headers=self.headers)

    def post(self, url, data={}):
        return self.client.post(url, data=json.dumps(data), headers=self.headers)

    def put(self, url, data={}):
        return self.client.put(url, data=json.dumps(data), headers=self.headers)

    def delete(self, url, data={}):
        return self.client.delete(url, data=json.dumps(data), headers=self.headers)


def json_loads_data(response, key=None):
    data = json.loads(response.get_data(as_text=True))
    return data.get(key) if key else data
