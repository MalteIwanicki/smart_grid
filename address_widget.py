# %%
import pathlib

import ipyvuetify as v
from util import get_coordinates

PTV_API_KEY = pathlib.Path("key.txt").read_text()


# %%
# Address
class Address(v.Container):
    def __init__(self):
        self.address_title = v.Subheader(children=["Address"])

        self.country = v.TextField(label="Land", v_model="", disabled=True)
        self.city = v.TextField(label="Stadt", v_model="", disabled=True)
        self.latitude = v.TextField(label="Latitude", v_model="", disabled=True)
        self.longitude = v.TextField(label="Longitude", v_model="", disabled=True)
        self.address_row = v.Col(
            children=[
                v.Row(children=[self.country]),
                v.Row(children=[self.city]),
                v.Row(children=[self.latitude]),
                v.Row(children=[self.longitude]),
            ],
        )

        self.search_address_text_field = v.TextField(
            label="Adresse", v_model="", prepend_inner_icon="mdi-map-marker"
        )
        self.search_address_text_field.on_event("change", self.get_address)

        self.address_card = v.Card(
            loading=False,
            elevation=0,
            children=[
                v.Row(children=[self.address_title]),
                v.Row(
                    children=[
                        v.Col(
                            cols=7,
                            children=[self.search_address_text_field],
                        ),
                        v.Col(
                            cols=5,
                            children=[self.address_row],
                        ),
                    ]
                ),
            ],
        )
        super().__init__(children=[self.address_card])

    def get_address(self, widget, event, data):
        self.address_card.loading = True
        self.coordinates = get_coordinates.get_coordinates(PTV_API_KEY, widget.v_model)
        self.country.v_model = self.coordinates["country"]
        self.city.v_model = self.coordinates["city"]
        self.latitude.v_model = self.coordinates["latitude"]
        self.longitude.v_model = self.coordinates["longitude"]
        self.next_btn.disabled = False
        self.address_card.loading = False


# %%
# Address()
