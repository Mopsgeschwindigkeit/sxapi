from sxapi.base import (
    BaseAPI,
    ApiTypes,
    PUBLIC_API_V2_BASE_URL,
)

from sxapi.publicV2.animal_lists import AnimalLists

class PublicAPIV2(BaseAPI):
    def __init__(self, base_url=None, email=None, password=None, api_token=None):
        """Initialize a new public api client instance."""
        base_url = base_url or PUBLIC_API_V2_BASE_URL
        api_type = ApiTypes.PUBLIC

        self.animal_lists = AnimalLists(api=self)

        super().__init__(
            base_url,
            email=email,
            password=password,
            api_token=api_token,
            api_type=api_type,
        )