# Human Development Reports (HDR) Dataset Analysis

This project involves explaratory data analysis (EDA) and statistical analysis of the HUman Development Reports (HDR) dataset, which provides insights into global human delevolpment metrics. The dataset was sourced from the [UNDP Data Center](https://hdr.undp.org/data-center/documentation-and-downloads).

## Table of contents
1. [Project Description](#project-description)
2. [Dataset](#dataset)
3. [Requirements](#requirements)
4. [Usage](#usage)
5. [Features](#features)
6. [Usage](#usage)
6. [Contributing](#contributing)
7. [License](#license)

## Project Description
The project aims to:
- Analyze trends in human development indices acros different countries and regions.
- Explore relationships between key indicators such as life expentancy, education levels, and income.
- Perform statistical analysis to identify patterns and correlations in the dataset.

## Dataset
The dataset was downloaded from the [UNDP Human Development Data Center](https://hdr.undp.org/data-center/documentation-and-downloads). It includes metrics such as:
- Human Development Index (HDI)
- Life expectancy at birth
- Expected and mean years of schooling
- Gross National Income (GNI) per capita
- GNI rank minus HDI rank

## Requirements
The following Python libraries are required:
- `pandas` for data manipulation and analysis
- `matplotlib` and `seaborn` for visualization
- `scikit-learn` for statistical and machine learning techniques
- `os` and `path` for file handling

To install the dependencies, run:
```bash
pip install pandas matplotlib seaborn scikit-learn
```
## Usage
1. Clone this repository:
```bash
git clone https://github.com/mohammedbehjoo/UN_HDR_data_analysis
```
2. Navigate to the project directory:
```bash
cd HDR_data_analysis
```
3. Download the dataset from the [UNDP website](https://hdr.undp.org/data-center/documentation-and-downloads) and sace it in the `data/` folder.
4. Run the analysis script:
```bash
python analyze_hdr.py
```
---
In order to make the dashboard run the following command in the terminal:

`streamlit run ./dashboard_intro.py --server.port 8888`

It will use the `8888` port for the connection in your local host.


## Features

- Preprocessing and cleaning of the HDR dataset.
- Statistical analysis of key indicators.
- Visualizations to showcase trends and relationships in the data.


## Contributing

Contributions are welcome! Feel free to submit a pull request or raise an issue for discussion.

## License

This project is licensed under the GNU V3 License. See the LICENSE file for details.
