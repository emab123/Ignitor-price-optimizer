import argparse, os
import pandas as pd
from math import ceil
from dataclasses import dataclass


@dataclass
class BatteryCell:
    """Data class to hold battery cell information."""
    name: str
    voltage: float
    max_current: float
    order_price: float
    order_qty: int
    shipping_cost: float  # Add shipping cost attribute
    link: str

@dataclass
class cable:
    """Data class to hold cable information."""
    name: str
    cross_section: float
    order_price: float
    order_qty: float
    shipping_cost: float  # Add shipping cost attribute
    link: str
    def __post_init__(self):
        self.linear_resistance = 1.68e-8 / (self.cross_section * 1e-6)  # Ohm per meter 
        self.resistance = lambda L: self.linear_resistance * L * 2  # Ohm (timdes 2 for round trip)


@dataclass
class skib:
    """Data class to hold skib information."""
    ignition_current: float
    resistance: float
    def __post_init__(self):
        self.ignition_voltage = self.ignition_current * self.resistance

def find_optimum(battery_cells: list[BatteryCell], cables: list[cable], skib: skib, distance: float):
    """Function to find the optimum battery cell and cable combination."""
    optimum = None
    i=0
    combinations=len(battery_cells)*len(cables)
    for cell in battery_cells:
        for cable in cables:
            i+=1
            voltage_drop = skib.ignition_voltage + (cable.resistance(distance) * skib.ignition_current)
            battery_cells_series = ceil(voltage_drop / cell.voltage/ cell.order_qty) * cell.order_qty 
            battery_cells_parallel = ceil(skib.ignition_current / cell.max_current)
            activation_current = battery_cells_series * cell.voltage / (cable.resistance(distance) + skib.resistance)
            battery_order_price = ceil(battery_cells_parallel * battery_cells_series / cell.order_qty) * cell.order_price 
            cable_order_price = ceil(distance / cable.order_qty) * cable.order_price
            total_order_price = (
                battery_order_price + cable_order_price + cell.shipping_cost + cable.shipping_cost
            )  # Include shipping costs
            if optimum is None or total_order_price < optimum['total_order_price']:
                optimum = {
                    'battery_cell': cell.name,
                    'cable': cable.name,
                    'cable_length': distance,
                    'cable_resistance': cable.resistance(distance),
                    'voltage_drop': voltage_drop,
                    'activation_current': activation_current,
                    'battery_cells_series': battery_cells_series,
                    'battery_voltage': cell.voltage*battery_cells_series,
                    'battery_cells_parallel': battery_cells_parallel,
                    'battery_order_price': battery_order_price+cell.shipping_cost,
                    'cable_order_price': cable_order_price+cable.shipping_cost,
                    'total_order_price': total_order_price,
                    'links': '\n\tBateria: ' + cell.link + '\n\tCabo: ' + cable.link
                }
                os.system('cls')
                print(f'\n\nTested {i}/{combinations}\nBest fit:\n')
                for key, value in optimum.items():
                    if isinstance(value, float):
                        print(f"{key}: {value:.2f}")
                    else:
                        print(f"\n{key}: {value}\n")


    return optimum

def main():
    """Main function to execute the program."""
    parser = argparse.ArgumentParser(description="Calculate the optimum configuration of battery cells and cables.")
    parser.add_argument("--battery_cells_file", type=str,default='batteries.csv', help="Path to the battery.csv file (default: battery.csv)")
    parser.add_argument("--cables_file", type=str, default='cables.csv',help="Path to the cables.csv file (default: cables.csv)")
    parser.add_argument("--distance", type=float, default=150, help="Distance in meters (default: 150 meters)")
    parser.add_argument("--skib_r", type=float, default=2, help="Skib Resistance (default: 2 Ohms)")
    parser.add_argument("--skib_i", type=float, default=3, help="Skib activation current (default: 3 Amps)")

    args = parser.parse_args()

    # Read battery cell information from the specified CSV file
    battery_cells_df = pd.read_csv(args.battery_cells_file)
    battery_cells = [
        BatteryCell(
            name=row['name'],
            voltage=row['voltage'],
            max_current=row['max_current'],
            order_price=row['order_price'],
            order_qty=row['order_qty'],
            shipping_cost=row['shipping_cost'],
            link=row['link']
        )
        for _, row in battery_cells_df.iterrows()
    ]

    # Read cable information from the specified CSV file
    cables_df = pd.read_csv(args.cables_file)
    cables = [
        cable(
            name=row['name'],
            cross_section=row['cross_section'],
            order_price=row['order_price'],
            order_qty=row['order_qty'],
            shipping_cost=row['shipping_cost'],
            link=row['link']
        )
        for _, row in cables_df.iterrows()
    ]

    skib1 = skib(
        ignition_current=args.skib_i,  # Example value in Amperes
        resistance=args.skib_r  # Example value in Ohms
    )

    # Calculate the optimum configuration
    optimum = find_optimum(battery_cells, cables, skib1, args.distance)
    if optimum:
        print('\n\nSuccesfully found optimum configuration.')
    else:
        print("\n\nNo optimum configuration found.")

if __name__ == "__main__":
    main()
