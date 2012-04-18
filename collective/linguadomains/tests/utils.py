class FakeContext:
    def __init__(self):
        self.lang = 'en'

    def Language(self):
        return self.lang

class FakeResponse:
    def __init__(self):
        self.redirect_url = None

    def redirect(self, url):
        self.redirect_url = url

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
