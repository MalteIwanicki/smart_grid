# %%
import requests


def get_photovoltaic_data(latitude, longitude, start_year=None, end_year=None):
    """
    Dokumentation:
    "https://joint-research-centre.ec.europa.eu/pvgis-photovoltaic-geographical-information-system/getting-started-pvgis/api-non-interactive-service_en"
    """
    response = requests.get(
        f"https://re.jrc.ec.europa.eu/api/seriescalc?lat={latitude}&lon={longitude}&horirrad=1&outputformat=json"
        f"{'&startyear='+str(start_year) if start_year else ''}"
        f"{'&endyear='+str(end_year) if end_year else ''}"
    )
    return response.json()["outputs"]["hourly"]
