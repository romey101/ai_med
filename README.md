# 🩺 Health & COVID Dashboard

An interactive data visualization dashboard built with **FastAPI** and **Plotly**, designed to track and compare yearly and quarterly trends in **COVID-19** and **infectious diseases** (e.g., Chickenpox, Pulmonary T.B., Leishmaniasis) from 2020 to 2023.

---

## 📌 Features

- 📈 **Line charts** for yearly trends and comparisons  
- 📊 **Bar charts** for new COVID cases, deaths, and vaccinations  
- 🔁 **Quarterly analysis** of COVID metrics  
- 🔄 **Dynamic metric switching** planned (totals vs. percent change)  
- 🧬 **Disease comparison** with COVID data on the same plot  
- 🎨 **Enhanced visualizations coming soon**:
  - Animated bar race charts  
  - Bubble plots  
  - Stacked area charts  
  - Heatmaps  
  - Pie and radial plots  

---

## 📁 Project Structure

```
ai_medical/
├── main.py                  # FastAPI app with all endpoints
├── app/
│   └── data/
│       ├── covid_saudi.csv          # Daily COVID data
│       └── diseases_in_years.csv    # Annual disease counts
├── requirements.txt
└── README.md
```

---

## 📊 Sample Dataset Fields

### `covid_saudi.csv` (daily records)

| Column             | Description                             |
|--------------------|-----------------------------------------|
| date               | Date of record                          |
| total_cases        | Cumulative COVID-19 cases               |
| total_deaths       | Cumulative COVID-19 deaths              |
| total_vaccinations | Cumulative vaccinations administered    |
| positive_rate      | Daily positive test rate (if available) |

### `diseases_in_years.csv` (annual totals)

| Column                 | Description                         |
|------------------------|-------------------------------------|
| Year                   | Year (2020 to 2023)                 |
| Chickenpox             | Total reported Chickenpox cases     |
| Pulmonary T.B.         | Total reported TB cases             |
| Visceral Leishmaniasis | Total reported Leishmaniasis cases |

---

## 🚀 How to Run the App

### 1. Clone the Repository

```bash
git clone https://github.com/your-username/ai_medical.git
cd ai_medical
```

### 2. Set Up Virtual Environment (optional but recommended)

```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

### 3. Install the Requirements

```bash
pip install -r requirements.txt
```

### 4. Launch the App

```bash
uvicorn main:app --reload
```

### 5. Open in Your Browser

```



---

✅ Built with ❤️ using FastAPI, Plotly, and pandas.
