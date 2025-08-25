# Ignitor Price Optimizer

This project helps you find the most cost-effective combination of battery cells and cables to ignite a skib.

### Prerequisites

* **Python**: Version 3.12 or newer is required.
* **Pipenv**: This project uses Pipenv for dependency management. If you don't have it installed, you can install it using pip:
    ```bash
    pip install pipenv
    ```

### Installation

1.  **Clone the Repository**: If you haven't already, clone the project repository from its source.
2.  **Navigate to the Project Directory**: Open your terminal or command prompt and change your current directory to the project's root folder.
3.  **Install Dependencies**: Use Pipenv to install all the necessary packages. This will read the `Pipfile.lock` file and create an isolated virtual environment with the exact versions of the dependencies:
    ```bash
    pipenv install
    ```

### Usage

1.  **Prepare your data**: The script requires two CSV files: `batteries.csv` and `cables.csv`. These files are listed in the `.gitignore` file, so they are not included in the repository. You need to create them and populate them with the data for your battery cells and cables. The script expects specific columns:
    * `batteries.csv`: `name`, `voltage`, `max_current`, `order_price`, `order_qty`, `shipping_cost`, `link`
    * `cables.csv`: `name`, `cross_section`, `order_price`, `order_qty`, `shipping_cost`, `link`
2.  **Run the script**: You can run the `optimizePrice.py` script using `pipenv run`. The script has a few optional arguments:
    * `--battery_cells_file`: Path to the battery CSV file (default: `batteries.csv`).
    * `--cables_file`: Path to the cables CSV file (default: `cables.csv`).
    * `--distance`: Distance in meters (default: 150).

    ```bash
    pipenv run python optimizePrice.py --distance 200
    ```
    This command will execute the script within the isolated virtual environment and calculate the optimum configuration for a distance of 200 meters. The output will display the results in the console.