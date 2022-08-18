# %%
from functools import cache
import ipyvuetify as v
import ipywidgets as widgets
from IPython.display import clear_output
import plotly.express as px
import numpy as np
from loguru import logger
from ipywidgets import jslink
from datetime import datetime

MONTHS = [
    "January",
    "February",
    "March",
    "April",
    "May",
    "June",
    "July",
    "August",
    "September",
    "October",
    "November",
    "December",
]


# %%
# PV
class Result(v.Container):
    def __init__(self, battery_container, pv_container, usage_container):
        self.res_title = v.Subheader(children=["Result"])
        self.battery_container = battery_container
        self.pv_container = pv_container
        self.usage_container = usage_container
        self.df = None
        self.month_selector = v.Select(
            v_model=0, label="month of Data", items=MONTHS, disabled=True
        )
        self.month_selector.on_event("change", self.select_month)
        self.days_without_public = v.TextField(
            label="days without public electricity", v_model="", disabled=True
        )
        self.days_with_public = v.TextField(
            label="days with public electricity", v_model="", disabled=True
        )
        self.total_sell = v.TextField(
            label="total sold electricity", v_model="", disabled=True
        )
        self.total_bought = v.TextField(
            label="total bought electricity", v_model="", disabled=True
        )
        self.average_battery_charge = v.TextField(
            label="average battery charge", v_model="", disabled=True
        )
        self.totals_row = v.Row(
            children=[
                v.Col(children=[self.days_with_public, self.days_without_public]),
                v.Col(children=[self.total_bought, self.total_sell]),
                v.Col(children=[self.average_battery_charge]),
            ]
        )
        self.card = v.Card(
            elevation=0,
            children=[
                v.Row(children=[self.res_title]),
                v.Row(children=[self.month_selector]),
            ],
        )

        super().__init__(children=[self.card, self.totals_row])

    @staticmethod
    def calc_production_surplus(row):
        p = row["production"]
        u = row["usage"]
        return p + u

    @staticmethod
    def calc_battery_charging(power, current_charge, battery_capacity):
        """
        Returns:
            float: How much the battery is charged or discharged (negative).
        """

        def charge():
            max_charging = battery_capacity - current_charge
            to_battery = min(max_charging, power)
            return to_battery

        def discharge():
            max_discharge = -current_charge
            from_battery = max(max_discharge, power)
            return from_battery

        return charge() if power > 0 else discharge()

    def prepare_df(self, production, usage, battery):
        df = production
        df["usage"] = usage["usage"]
        df["production_surplus"] = df.apply(Result.calc_production_surplus, axis=1)

        df["charge"] = 0
        df["to_battery"] = 0
        df["to_system"] = 0
        battery_capacity = float(battery.capacity)
        for i in df.index:
            power = df.loc[i, "production_surplus"]
            current_charge = df.loc[i - 1, "charge"] if i != 0 else 0
            to_battery = Result.calc_battery_charging(
                power, current_charge, battery_capacity
            )
            df.loc[i, "to_battery"] = to_battery
            df.loc[i, "charge"] = current_charge + to_battery
            df.loc[i, "to_system"] = power - to_battery
        return df

    def load(self):
        self.card.loading = True
        logger.info("collect_data")
        b, p, u = self.collect_data()
        self.battery = b
        logger.info("prep_df")
        self.df = self.prepare_df(p, u, b)

        logger.info("split_df")
        self.dfs = self.split_df(self.df)
        self.month_selector.disabled = False
        self.days_with_public.v_model = self.get_days_with_public()
        self.days_without_public.v_model = self.get_days_without_public()
        self.total_bought.v_model = self.get_total_bought()
        self.total_sell.v_model = self.get_total_sell()
        self.average_battery_charge.v_model = self.get_average_battery_charge()
        self.card.loading = False

    def get_days_with_public(self):
        df = self.df
        days_with_public = {}
        for _, row in df.iterrows():
            date = datetime.strptime(row["date"], "%Y-%m-%d %H").strftime("%j")
            days_with_public.setdefault(date, False)
            days_with_public[date] = (
                True if row["to_system"] < 0 or days_with_public[date] else False
            )
        out = sum(days_with_public.values())
        return out

    def get_days_without_public(self):
        df = self.df
        days_with_public = {}
        for _, row in df.iterrows():
            date = datetime.strptime(row["date"], "%Y-%m-%d %H").strftime("%j")
            days_with_public.setdefault(date, False)
            days_with_public[date] = (
                True if row["to_system"] < 0 or days_with_public[date] else False
            )
        out = len(days_with_public) - sum(days_with_public.values())
        return out

    def get_total_bought(self):
        df = self.df
        total = 0
        for _, row in df.iterrows():
            if row["to_system"] < 0:
                total += row["to_system"]
        return round(-total, 2)

    def get_total_sell(self):
        df = self.df
        total = 0
        for _, row in df.iterrows():
            if row["to_system"] > 0:
                total += row["to_system"]
        return round(total, 2)

    def get_average_battery_charge(self):
        df = self.df
        total = 0
        for _, row in df.iterrows():
            total += float(row["charge"])
        average = total / df.shape[0]
        percentile = 100 / self.battery["capacity"] * average
        return round(percentile, 2)

    def select_month(self, *args):
        self.card.loading = True
        month_index = MONTHS.index(self.month_selector.v_model)
        self.children = [
            self.card,
            self.get_fig(self.dfs[month_index]),
            self.totals_row,
        ]
        self.card.loading = False

    def split_df(self, df):
        partitions = 12
        return np.array_split(df, partitions)

    @cache
    def collect_data(self):
        battery = self.battery_container.battery.copy()
        production = self.pv_container.pv_power_data.copy()
        usage = self.usage_container.usage_profile.copy()
        return battery, production, usage

    def get_fig(self, df):
        plot = widgets.Output()
        with plot:
            clear_output(wait=True)
            fig = px.bar(
                df,
                x="date",
                y=["charge", "to_system"],
            )
            fig.update_xaxes(
                rangeslider_visible=True,
                rangeselector=dict(
                    buttons=list(
                        [
                            dict(
                                count=24, label="1d", step="hour", stepmode="backward"
                            ),
                            dict(count=7, label="1w", step="day", stepmode="backward"),
                            dict(step="all"),
                        ]
                    )
                ),
            )
            fig.show(renderer="notebook")
        return plot


# %%
