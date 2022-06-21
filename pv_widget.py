# %%
import ipyvuetify as v
from ipywidgets import jslink


# %%
# PV
class Photovoltaic(v.Container):
    def __init__(self):
        self.pv_title = v.Subheader(children=["Photovoltaic"])

        self.pv_peak_power = v.TextField(
            label="Installed peak power in Wp",
            reverse=True,
            type="number",
            v_model="1000",
        )
        self.pv_slope = v.Slider(v_model=45, max=90, min=0)
        self.pv_slope_text = v.TextField(
            label="Slope in °",
            v_model="",
            type="number",
            reverse=True,
            style_="text_align:right;",
        )
        jslink((self.pv_slope, "v_model"), (self.pv_slope_text, "v_model"))

        self.pv_azimuth = v.Slider(
            v_model=180,
            max=359,
            min=0,
        )
        self.pv_azimuth_text = v.TextField(
            label="Azimuth in °", v_model="", type="number", reverse=True
        )
        jslink((self.pv_azimuth, "v_model"), (self.pv_azimuth_text, "v_model"))

        pv_card = v.Card(
            elevation=0,
            children=[
                v.Row(children=[self.pv_title]),
                v.Row(
                    children=[
                        v.Col(cols=3, children=[self.pv_peak_power]),
                        v.Col(cols=9),
                    ]
                ),
                v.Row(
                    children=[
                        v.Col(cols=3, children=[self.pv_slope_text]),
                        v.Col(cols=9, children=[self.pv_slope]),
                    ]
                ),
                v.Row(
                    children=[
                        v.Col(cols=3, children=[self.pv_azimuth_text]),
                        v.Col(cols=9, children=[self.pv_azimuth]),
                    ]
                ),
            ],
        )
        super().__init__(children=[pv_card])


# %%
# Photovoltaic()

# %%
