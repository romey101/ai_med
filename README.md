# 🩺 Health & COVID Dashboard

An interactive data visualization dashboard built with **FastAPI** and **Plotly**, designed to track and analyze yearly trends of COVID-19 and other infectious diseases from 2020 to 2023.

## 📌 Features

- 📈 **Line charts** showing annual percentage changes in disease metrics
- 📊 **Bar charts** displaying raw counts of COVID cases, deaths, vaccinations, and more
- 🔄 **Dynamic metric switching** between raw totals and percent change
- 🎨 **Enhanced visuals** planned: animated bar charts, bubble charts, pie charts, stacked area, and heatmaps

## 📁 Project Structure


app/
│
├── data/
│ └── gathered_insights.csv # Source CSV file (raw and % change data)
│ └── output_dataset.csv # Cleaned + processed CSV (used in app)
│
├── routes/
│ └── plots.py # Extra charts (multi-line % change, etc.)
│
├── templates/
│ ├── dashboard.html # Main dashboard with dropdowns
│ └── plot.html # Chart-only template
│
├── static/ # (Optional) Static assets (CSS/images if added)
│
main.py # App entrypoint with root route


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
