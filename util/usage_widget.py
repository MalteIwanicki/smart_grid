# %%
from faulthandler import disable
import pandas as pd
import ipyvuetify as v
import ipywidgets as widgets
from IPython.display import clear_output
import plotly.express as px

USAGE_FILE = "data/usage.json"


# %%
usage_df = pd.read_json(USAGE_FILE).set_index("id")
usage_names = list(usage_df.index)


class Usage(v.Container):
    def __init__(self):
        self.usage_profile = None
        self.usage_title = v.Subheader(children=["Usage"])
        self.usage_input = v.TextField(
            label="Yearly usage in kWh/a",
            reverse=True,
            type="number",
            v_model="1",
        )
        self.usage_factor = v.TextField(
            label="Factor",
            reverse=True,
            type="number",
            disabled=True,
            v_model="0",
        )
        self.usage_input.on_event("change", self.usage_change)

        self.usage_select = v.Select(
            label="Usage Profile", v_model="", items=usage_names
        )
        self.usage_select.on_event("change", self.usage_change)

        self.usage_card = v.Card(
            loading=False,
            elevation=0,
            children=[
                v.Row(children=[self.usage_title]),
                v.Row(
                    children=[
                        v.Col(
                            cols=7,
                            children=[self.usage_select],
                        ),
                        v.Col(cols=5, children=[self.usage_input]),
                    ]
                ),
                v.Row(children=[self.usage_factor]),
            ],
        )
        super().__init__(children=[self.usage_card])

    def get_usage_fig(self):
        df = self.usage_profile
        df["usage"] = -df["usage"]
        plot = widgets.Output()
        with plot:
            clear_output(wait=True)
            fig = px.line(df, x="date", y="usage")
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

    def get_factor(self):
        return (
            int(self.usage_input.v_model) * 1000 / self.usage_base
        )  # *1000 so its in W not kw

    def usage_change(self, widget, *args):
        self.usage_card.loading = True
        self.file = usage_df.loc[self.usage_select.v_model]["file"]
        self.usage_base = usage_df.loc[self.usage_select.v_model]["base"]
        self.usage_profile = pd.read_parquet(self.file)
        self.usage_factor.v_model = self.get_factor()
        self.usage_profile["usage"] = self.usage_profile.apply(
            lambda row: row["usage"] * self.get_factor(), axis=1
        )
        self.children = [self.usage_card, self.get_usage_fig()]
        self.next_btn.disabled = False
        self.usage_card.loading = False


# %%
