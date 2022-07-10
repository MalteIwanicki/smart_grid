# %%
import statistics

import pandas as pd
import ipyvuetify as v
import ipywidgets
from matplotlib import pyplot as plt

USAGE_FILE = "data/usage.json"


# %%
usage_df = pd.read_json(USAGE_FILE).set_index("id")
usage_names = list(usage_df.index)


class Usage(v.Container):
    def __init__(self):
        self.usage_profile = None
        self.usage_title = v.Subheader(children=["Usage"])

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
                        )
                    ]
                ),
            ],
        )
        super().__init__(children=[self.usage_card])

    def get_usage_fig(self):
        x = [day for day in self.usage_profile.index[::5]]
        y = [sum(day) for day in self.usage_profile.values]
        y = [
            statistics.mean(values)
            for values in zip(y[::5], y[1::5], y[2::5], y[3::5], y[4::5])
        ]
        plot = ipywidgets.Output()
        with plot as out:
            fig, ax = plt.subplots(figsize=(10, 10))
            ax.plot(x, y)
            plt.show()
        return plot

    def usage_change(self, widget, *args):
        self.usage_card.loading = True
        self.file = usage_df.loc[self.usage_select.v_model]["file"]
        self.usage_profile = pd.read_parquet(self.file)
        self.children = [self.usage_card, self.get_usage_fig()]
        # self.next_btn.disabled = False
        self.usage_card.loading = False


# %%
