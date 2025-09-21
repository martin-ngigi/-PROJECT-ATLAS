import logging

import pandas as pd
from .nasa import services as nasa_service
from .ncei import services as ncei_service
from .open_meteo import services as open_meteo_service
from .models import ClimateTemperature
from datetime import datetime

def _normalize_to_df(source_name: str, data: dict) -> pd.DataFrame:
    """
    Convert nested dict {year: {year-month: value}} to DataFrame.
    """
    records = []
    for year, months in data.items():
        for month, value in months.items():
            records.append({"date": month, source_name: value})
        return pd.DataFrame(records).set_index("date")
    
def aggregare_monthly_avg_temperature(nasa_kwargs, ncei_kwargs, open_meteo_kwargs):
    """
    Fetch monthly average temperature from NASA, NCEI and Open Meteo,
    aggregate into a singlr DataFrame and save to DB.
    """

    # Fetch data from service 
    nasa_data = nasa_service.get_monthly_avg_temperature(**nasa_kwargs)
    # ncei_data = ncei_service.get_monthly_avg_temperature(**ncei_kwargs)
    open_meteo_data = open_meteo_service.get_monthly_avg_temperature(**open_meteo_kwargs)

    # Normalize data to DataFrame
    df_nasa = _normalize_to_df("nasa", nasa_data)
    # df_ncei = _normalize_to_df("ncei", ncei_data)
    df_open_meteo = _normalize_to_df("open_meteo", open_meteo_data)

    # Merge all sources on "date"
    # combined = pd.concat([df_nasa, df_ncei, df_open_meteo], axis=1)
    combined = pd.concat([df_nasa, df_open_meteo], axis=1)

    # Compute row-wise mean across sources
    combined["mean"] = combined.mean(axis=1, skipna=True).round(2)

    #Group by year and save each row to DB
    result = {}
    for date, row in combined.iterrows():

        year = int(date.split("-")[0]) #Extract Year from "YYYY-MM"
        month = int(date.split("-")[1])

        #Create date object for the first day of the month
        month_date = datetime(year, month, 1).date()

        obj, created = ClimateTemperature.objects.update_or_create(
            #Fields to check for existing record.
            longitude=open_meteo_kwargs["longitude"],
            latitude=open_meteo_kwargs["latitude"],
            month=month,
            year=year,

            #Fields to update if record exists or create if new
            defaults={
                'start_date': open_meteo_kwargs["start_date"],
                'end_date': open_meteo_kwargs["end_date"],
                'open_meteo_value': row.get("open_meteo"),
                'nasa_value': row.get("nasa"),
                'ncei_value': row.get("ncei"),
                'mean_value': row.get("mean"),
                'value': row.get("mean"),
                'measurement_unit': "T2M",
                'unit_standardized': "Celsius",
                'source': "aggregated",
                'aggregation_method': "mean",
                'country': ""
            }
        )

        """   
       ClimateTemperature.objects.create(
            longitude=open_meteo_kwargs["longitude"],
            latitude=open_meteo_kwargs["latitude"],
            year=year,
            start_date=open_meteo_kwargs["start_date"],
            end_date=open_meteo_kwargs["end_date"],
            open_meteo_value=row.get("open_meteo"),
            nasa_value=row.get("nasa"),
            ncei_value=row.get("ncei"),
            mean_value=row.get("mean"),
            value=row.get("mean"),
            measurement_unit = "T2M",
            unit_standardized = "Celsius",
            source = "aggregated",
            aggregation_method = "mean",
            country = ""
        )
        """
        logging.info(f"✅ SUCCESS: Created/Updated ClimateTemperature {created} successfully.")

        # Build nested result
        year_str = str(year)
        if year_str not in result:
            result[year_str] = {}
        result[year_str][date] = {
            "nasa": row.get("nasa"),
            "open_meteo": row.get("open_meteo"),
            # "ncei": row.get("ncei"),
            "mean": row.get("mean")
        }

    # Return combined aggregated results as dict
    return result

