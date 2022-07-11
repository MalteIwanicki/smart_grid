# %%
import ipyvuetify as v
import ipywidgets as widgets
from IPython.display import clear_output
import plotly.express as px

from ipywidgets import jslink


# %%
# PV
class Photovoltaic(v.Container):
    def __init__(self):
        self.pv_title = v.Subheader(children=["Photovoltaic"])
        self.pv_power_data = []
        self.pv_technology = v.Select(
            v_model="",
            label="PV technology used",
            items=["crystSi", "CIS", "CdTe", "Unknown"],  # TODO beschreiben im word.
        )

        def select_pv(widget, *args):
            self.calc_btn.disabled = False

        self.pv_technology.on_event("change", select_pv)

        self.pv_peak_power = v.TextField(
            label="Installed peak power in kWp",
            reverse=True,
            type="number",
            v_model="1",
        )
        self.pv_loss = v.Slider(v_model=14, max=100, min=0)
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

        self.pv_card = v.Card(
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
        super().__init__(children=[self.pv_card])

    def get_fig(self):
        df = self.pv_power_data

        plot = widgets.Output()
        with plot:
            clear_output(wait=True)
            fig = px.line(df, x="date", y="production")
            fig.update_xaxes(
                rangeslider_visible=True,
                rangeselector=dict(
                    buttons=list(
                        [
                            dict(
                                count=24, label="1d", step="hour", stepmode="backward"
                            ),
                            dict(count=7, label="1w", step="day", stepmode="backward"),
                            dict(
                                count=1, label="1m", step="month", stepmode="backward"
                            ),
                            dict(
                                count=6, label="6m", step="month", stepmode="backward"
                            ),
                            dict(step="all"),
                        ]
                    )
                ),
            )
            fig.show(renderer="notebook")
        return plot

    def get_days_average(self, hourly_data):
        days_average = {}
        for hour in hourly_data:
            day_key = hour["time"].split(":")[0]
            days_average.setdefault(day_key, 0)
            days_average[day_key] += 1 / 24 * hour["PV system power"]
        days_average = [
            {"time": key, "PV system power": val} for key, val in days_average.items()
        ]
        return days_average


# %%
# Photovoltaic()

# %%
