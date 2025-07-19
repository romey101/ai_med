# 🩺 Health & COVID Dashboard

An interactive data visualization dashboard built with **FastAPI** and **Plotly**, designed to track and analyze yearly trends of COVID-19 and other infectious diseases from 2020 to 2023.

## 📌 Features

- 📈 **Line charts** showing annual percentage changes in disease metrics
- 📊 **Bar charts** displaying raw counts of COVID cases, deaths, vaccinations, and more
- 🔄 **Dynamic metric switching** between raw totals and percent change
- 🎨 **Enhanced visuals** planned: animated bar charts, bubble charts, pie charts, stacked area, and heatmaps

## 📁 Project Structure


ai_medical/
├── main.py
├── app/
│   └── data/
│       ├── covid_saudi.csv
│       └── diseases_in_years.csv



## 🧪 Sample Dataset Columns

| Column                          | Description                            |
|----------------------------------|----------------------------------------|
| Year                            | Year (2020–2023)                       |
| Total COVID Cases               | Raw case count                         |
| COVID Deaths                    | Raw death count                        |
| COVID Vaccinations              | Raw vaccination count                  |
| Chickenpox, Pulmonary T.B., ... | Other diseases                         |
| ... % Change                    | Year-over-year % change for each field |

## 🚀 How to Run

### 1. Install Dependencies
Make sure you are using Python 3.8 or later.

```bash
pip install -r requirements.txt
fastapi
uvicorn
pandas
plotly
jinja2
