from urllib.parse import urlencode


class AnimalLists:

    def __init__(self, api):
        self.api = api
        self.base_url_suffix = "/animal_lists"

    def post_animal_lists(self, organisation_id, name, rule):
        params = {
            "organisation_id": organisation_id,
            "name": name,
            "rule": rule,
        }

        path = self.base_url_suffix
        return self.api.post(path, json=params)
