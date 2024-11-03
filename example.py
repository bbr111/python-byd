"""Sample code to use the wrapper for interacting with the BYDHVS API."""
import asyncio
from bydhvs import BYDHVS

byd_host = "192.168.16.254"
byd_port = 8080


async def main():
    """The main part of the example script."""
    batt = BYDHVS(byd_host, byd_port)
    #Get the data
    await batt.poll()

    data = batt.get_data()

    print("BYD HVS Batteriedaten:")
    print(f"Seriennummer: {data['serial_number']}")
    print(f"BMU Firmware: {data['bmu_firmware']}")
    print(f"BMS Firmware: {data['bms_firmware']}")
    print(f"Module: {data['modules']}")
    print(f"Türme: {data['towers']}")
    print(f"Netztyp: {data['grid_type']}")
    print(f"SOC: {data['soc']}%")
    print(f"Maximale Spannung: {data['max_voltage']} V")
    print(f"Minimale Spannung: {data['min_voltage']} V")
    print(f"SOH: {data['soh']}%")
    print(f"Strom: {data['current']} A")
    print(f"Batteriespannung: {data['battery_voltage']} V")
    print(f"Höchste Temperatur: {data['max_temperature']} °C")
    print(f"Niedrigste Temperatur: {data['min_temperature']} °C")
    print(f"Leistung: {data['power']} W")
    print(f"Fehler: {data['error']}")
    print(f"Anzahl der Balancing-Zellen: {data['balancing_count']}")
    print("Einzelzellenspannungen (mV):")
    for idx, voltage in enumerate(data['cell_voltages'], start=1):
        print(f"  Zelle {idx}: {voltage} mV")
    print("Einzelzellentemperaturen (°C):")
    for idx, temp in enumerate(data['cell_temperatures'], start=1):
        print(f"  Zelle {idx}: {temp} °C")

if __name__ == "__main__":
    asyncio.run(main())