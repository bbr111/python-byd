"""Sample code to use the wrapper for interacting with the BYD API."""
import asyncio
from byd import byd

byd_host = "192.168.16.254"
byd_port = "8080"


async def main():
    """The main part of the example script."""
    batt = byd(byd_host, byd_port)
    #Get the data
    batt.read_data()

    print("serial:", batt.hvs_serial)
    print("hvs_batt_type_from_serial", batt.hvs_batt_type_from_serial)
    print("bmu", batt.hvs_bmu)
    print("bms", batt.hvs_bms)
    print("modules", batt.hvs_modules)
    print("grid", batt.hvs_grid)
    print("soc", batt.soc)
    print("maxvolt", batt.maxvolt)
    print("minvolt", batt.minvolt)
    print("soh", batt.soh)
    print("ampere", batt.ampere)
    print("battvolt", batt.battvolt)
    print("maxtemp", batt.maxtemp)
    print("mintemp", batt.mintemp)
    print("battemp", batt.battemp)
    print("error", batt.error)
    print("paramt", batt.paramt)
    print("outvolt", batt.outvolt)
    print("power", batt.power)
    print("diffvolt", batt.diffvolt)
    print("hvsMaxmVolt", batt.hvsMaxmVolt)
    print("hvsMinmVolt", batt.hvsMinmVolt)
    print("hvsMaxmVoltCell", batt.hvsMaxmVoltCell)
    print("hvsMinmVoltCell", batt.hvsMinmVoltCell)
    print("hvsMaxTempCell", batt.hvsMaxTempCell)
    print("hvsMinTempCell", batt.hvsMinTempCell)
    print("hvsSOCDiagnosis", batt.hvsSOCDiagnosis)
    print("hvs_battery_volts_per_cell", batt.hvs_battery_volts_per_cell)
    print("hvs_battery_temps_per_cell", batt.hvs_battery_temps_per_cell)

if __name__ == "__main__":
    asyncio.run(main())