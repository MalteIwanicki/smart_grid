from types import SimpleNamespace
from datetime import datetime
import pandas as pd
import util.result_widget


def test_calc_production_surplus():
    assert (
        util.result_widget.Result.calc_production_surplus(
            {"production": 10, "usage": -4}
        )
        == 6
    )


def test_calc_battery_charging():
    # charge
    ## filling up
    assert (
        util.result_widget.Result.calc_battery_charging(
            power=10,
            current_charge=2,
            battery_capacity=6,
        )
        == 4
    )
    ## not Filling up
    assert (
        util.result_widget.Result.calc_battery_charging(
            power=2,
            current_charge=2,
            battery_capacity=6,
        )
        == 2
    )
    # Discharge
    ## emptying
    assert (
        util.result_widget.Result.calc_battery_charging(
            power=-10,
            current_charge=4,
            battery_capacity=-6,
        )
        == -4
    )
    ## not emptying
    assert (
        util.result_widget.Result.calc_battery_charging(
            power=-5,
            current_charge=6,
            battery_capacity=6,
        )
        == -5
    )


def test_prepare_df():
    production = pd.DataFrame({"production": [5, 6, 10, 0, 0]})
    usage = {"usage": [-4, -5, -5, -4, -10]}
    battery = SimpleNamespace(capacity=6)
    assert util.result_widget.Result.prepare_df(
        util.result_widget.Result, production, usage, battery
    ).iloc[-1].tolist() == [0, -10, -10, 0, -2, -8]


def test_get_days_with_public():
    df = pd.DataFrame(
        {
            "date": [
                "2022-01-01 01",
                "2022-01-01 02",
                "2022-01-02 01",
                "2022-01-03 01",
                "2022-01-04 01",
            ],
            "to_system": [-1, -2, 0, -10, 5],
        }
    )
    dummy = SimpleNamespace(df=df)
    assert util.result_widget.Result.get_days_with_public(dummy) == 2


def test_get_days_without_public():
    df = pd.DataFrame(
        {
            "date": [
                "2022-01-01 01",
                "2022-01-01 02",
                "2022-01-02 01",
                "2022-01-03 01",
                "2022-01-04 01",
            ],
            "to_system": [-1, -2, 0, -10, 5],
        }
    )
    dummy = SimpleNamespace(df=df)
    assert util.result_widget.Result.get_days_without_public(dummy) == 2


def test_get_total_bought():
    df = pd.DataFrame(
        {
            "date": [
                "2022-01-01 01",
                "2022-01-01 02",
                "2022-01-02 01",
                "2022-01-03 01",
                "2022-01-04 01",
            ],
            "to_system": [-1, -2, 0, -10, 5],
        }
    )
    dummy = SimpleNamespace(df=df)
    assert util.result_widget.Result.get_total_bought(dummy) == 13


def test_get_total_sell():
    df = pd.DataFrame(
        {
            "date": [
                "2022-01-01 01",
                "2022-01-01 02",
                "2022-01-02 01",
                "2022-01-03 01",
                "2022-01-04 01",
            ],
            "to_system": [-1, -2, 0, 1, 5],
        }
    )
    dummy = SimpleNamespace(df=df)
    assert util.result_widget.Result.get_total_sell(dummy) == 6


def test_get_average_battery_charge():
    df = pd.DataFrame(
        {
            "charge": [2, 2, 2, 0, 0, 0],
        }
    )
    battery = {"capacity": 10}
    dummy = SimpleNamespace(df=df, battery=battery)
    assert util.result_widget.Result.get_average_battery_charge(dummy) == 10.0
