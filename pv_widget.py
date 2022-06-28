# %%
import ipyvuetify as v
from ipywidgets import jslink


# %%
# PV
class Photovoltaic(v.Container):
    def __init__(self):
        self.pv_title = v.Subheader(children=["Photovoltaic"])

        self.pv_technology = v.Select(
            v_model="",
            label="PV technology used",
            items=["crytSi", "CIS", "CdTe", "Unknown"],
        )

        def select_pv(widget, *args):
            self.next_btn.disabled = False

        self.pv_technology.on_event("change", select_pv)

        self.pv_peak_power = v.TextField(
            label="Installed peak power in kWp",
            reverse=True,
            type="number",
            v_model="1",
        )
        self.pv_loss = v.Slider(v_model=0, max=100, min=0)
        self.pv_loss_text = v.TextField(
            label="System loss in %",
            v_model="",
            type="number",
            reverse=True,
            style_="text_align:right;",
        )
        jslink((self.pv_loss, "v_model"), (self.pv_loss_text, "v_model"))

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
                        v.Col(cols=3, children=[self.pv_technology]),
                        v.Col(cols=9),
                    ]
                ),
                v.Row(
                    children=[
                        v.Col(cols=3, children=[self.pv_peak_power]),
                        v.Col(cols=9),
                    ]
                ),
                v.Row(
                    children=[
                        v.Col(cols=3, children=[self.pv_loss_text]),
                        v.Col(cols=9, children=[self.pv_loss]),
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
Photovoltaic()

# %%
