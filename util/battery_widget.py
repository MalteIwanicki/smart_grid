# %%
import pandas as pd
import ipyvuetify as v

BATTERIES_FILE = "data/batteries.json"


# %%
# Battery
battery_df = pd.read_json(BATTERIES_FILE).set_index("id").sort_values("efficiency_rank")
battery_names = list(battery_df["name"])
# battery_df.head(2)


class Battery(v.Container):
    def __init__(self):
        self.battery = None
        self.battery_title = v.Subheader(children=["Battery"])

        self.battery_ranking = v.TextField(
            label="Efficiency ranking", v_model="", disabled=True
        )
        self.battery_type = v.TextField(label="Type", v_model="", disabled=True)
        self.battery_capacity = v.TextField(
            label="Capacity", v_model="", disabled=True, suffix="W"
        )
        self.battery_average_efficiency = v.TextField(
            label="Average efficiency", v_model="", disabled=True
        )

        self.battery_row = v.Col(
            children=[
                v.Row(children=[self.battery_ranking]),
                v.Row(children=[self.battery_type]),
                v.Row(children=[self.battery_capacity]),
                v.Row(children=[self.battery_average_efficiency]),
            ],
        )
        self.battery_select = v.Select(label="Battery", v_model="", items=battery_names)
        self.battery_select.on_event("change", self.battery_change)

        self.battery_card = v.Card(
            loading=False,
            elevation=0,
            children=[
                v.Row(children=[self.battery_title]),
                v.Row(
                    children=[
                        v.Col(
                            cols=7,
                            children=[self.battery_select],
                        ),
                        v.Col(
                            cols=5,
                            children=[self.battery_row],
                        ),
                    ]
                ),
            ],
        )
        super().__init__(children=[self.battery_card])

    def battery_change(self, widget, *args):
        self.battery_card.loading = True
        self.battery = battery_df.loc[battery_df["name"] == widget.v_model]
        self.battery_ranking.v_model = str(self.battery["efficiency_rank"].values[0])
        self.battery_type.v_model = str(self.battery["type"].values[0])
        self.battery_capacity.v_model = str(self.battery["capacity"].values[0])
        self.battery_average_efficiency.v_model = str(
            round(self.battery["average_efficiency"].values[0], 4)
        )
        self.next_btn.disabled = False
        self.battery_card.loading = False


# get photovoltaic data
# data = get_photovoltaic_data(coordinates["latitude"],coordinates["longitude"])
# data_text.v_model = (
#     f'{data}'
# )


# %%
# Battery()

# %%
