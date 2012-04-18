class FakeResponse:
    def __init__(self):
        self.next_url = None

    def redirect(self, url):
        self.next_url = url

class FakeRequest:
    def __init__(self):
        self.RESPONSE = FakeResponse()
        self._data = {'ACTUAL_URL':'http://nohost-fr/plone/news'}

    def get(self, key):
        return self._data.get(key)

class FakeSettings:
    def __init__(self):
        self.activated = True
        self.mapping = ['http://nohost-en/plone|en',
                        'http://nohost-fr/plone|fr',
                        'http://nohost-nl/plone|nl']

class FakeEvent:
    def __init__(self):
        self.request = FakeRequest()
        self.tests = {}
        self.tests['purl'] = 'http://nohost-en/plone'
        self.tests['lang'] = 'en'
        self.tests['settings'] = FakeSettings()
