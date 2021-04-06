from bootstrap import load_json
from requests import Request, Session

config = load_json()


class Alert:

    def get_headers(self):
        """returns headers"""

        headers = {
            'Accepts': 'application/json',
            'X-CMC_PRO_API_KEY': config.get('API_KEY')
        }

        return headers

    def start_session(self):
        session = Session()
        session.headers.update(self.get_headers())
        return session
