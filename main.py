from fastapi import FastAPI
from fastapi.responses import HTMLResponse
import pandas as pd
import plotly.express as px

app = FastAPI()

# ---------------- Load COVID Yearly Data ---------------- #
def load_yearly_data():
    df = pd.read_csv("app/data/covid_saudi.csv", parse_dates=["date"])
    df = df.sort_values("date")
    df['year'] = df['date'].dt.year

    yearly = df.groupby('year').agg({
        'total_cases': 'last',
        'total_deaths': 'last',
        'total_vaccinations': 'last',
        'positive_rate': 'mean'
    }).dropna(subset=['total_cases', 'total_deaths']).reset_index()

    yearly[['new_cases', 'new_deaths', 'new_vaccinations']] = yearly[
        ['total_cases', 'total_deaths', 'total_vaccinations']
    ].diff().fillna(0)

    return yearly

# ---------------- Load COVID Quarterly Data ---------------- #
def load_quarterly_data():
    df = pd.read_csv("app/data/covid_saudi.csv", parse_dates=["date"])
    df = df.sort_values("date")
    df['quarter'] = df['date'].dt.to_period("Q").astype(str)

    quarterly = df.groupby('quarter').agg({
        'total_cases': 'last',
        'total_deaths': 'last',
        'total_vaccinations': 'last'
    }).dropna(subset=['total_cases', 'total_deaths']).reset_index()

    quarterly[['new_cases', 'new_deaths', 'new_vaccinations']] = quarterly[
        ['total_cases', 'total_deaths', 'total_vaccinations']
    ].diff().fillna(0)

    return quarterly

# ---------------- Merge with Disease Data ---------------- #
def load_combined_disease_data():
    covid = load_yearly_data()
    disease = pd.read_csv("/Users/maram/ai_medical/app/data/diseases in years.csv")
    disease.columns = disease.columns.str.strip()
    disease['Year'] = pd.to_numeric(disease['Year'], errors='coerce')
    disease = disease.rename(columns={"Year": "year"})

    for col in ['Chickenpox', 'Pulmonary T.B.', 'Visceral Leishmaniasis']:
        disease[col] = disease[col].astype(str).str.replace(",", "").astype(int)

    merged = pd.merge(covid, disease, on="year", how="inner")

    melted = merged.melt(
        id_vars="year",
        value_vars=["new_cases", "new_vaccinations", "Chickenpox", "Pulmonary T.B.", "Visceral Leishmaniasis"],
        var_name="condition",
        value_name="count"
    )

    return melted

# ---------------- Home UI ---------------- #
@app.get("/", response_class=HTMLResponse)
async def root():
    return """
    <html>
    <head>
        <title>COVID Dashboard</title>
        <style>
            body { font-family: Arial; text-align: center; margin-top: 80px; background: #f4f4f4; }
            .container {
                background: white;
                padding: 40px;
                border-radius: 12px;
                box-shadow: 0 4px 12px rgba(0,0,0,0.1);
                display: inline-block;
            }
            select {
                font-size: 18px;
                padding: 10px;
                margin-top: 20px;
            }
        </style>
    </head>
    <body>
        <div class="container">
            <h2>COVID-19 & Disease Dashboard</h2>
            <select onchange="window.location.href=this.value">
                <option value="">-- Select Visualization --</option>
                <option value="/cases_chart">Yearly New COVID Cases</option>
                <option value="/deaths_chart">Yearly New COVID Deaths</option>
                <option value="/vaccinations_chart">Yearly New Vaccinations</option>
                <option value="/positive_rate_chart">Positive Rate per Year</option>
                <option value="/quarterly_chart">Quarterly COVID Insights</option>
                <option value="/disease_comparison">COVID vs Disease Comparison</option>
                <option value="/vaccine_line_chart">Daily New Cases & Deaths (Before vs After Vaccine)</option>
            </select>
        </div>
    </body>
    </html>
    """

# ---------------- Individual Endpoints ---------------- #
@app.get("/cases_chart", response_class=HTMLResponse)
async def cases_chart():
    yearly = load_yearly_data()
    fig = px.bar(yearly, x='year', y='new_cases', title="Yearly New COVID Cases")
    return HTMLResponse(fig.to_html(include_plotlyjs='cdn'))

@app.get("/deaths_chart", response_class=HTMLResponse)
async def deaths_chart():
    yearly = load_yearly_data()
    fig = px.bar(yearly, x='year', y='new_deaths', title="Yearly New COVID Deaths")
    return HTMLResponse(fig.to_html(include_plotlyjs='cdn'))

@app.get("/vaccinations_chart", response_class=HTMLResponse)
async def vaccinations_chart():
    yearly = load_yearly_data()
    fig = px.bar(yearly, x='year', y='new_vaccinations', title="Yearly New Vaccinations")
    return HTMLResponse(fig.to_html(include_plotlyjs='cdn'))

@app.get("/positive_rate_chart", response_class=HTMLResponse)
async def positive_rate_chart():
    yearly = load_yearly_data()
    fig = px.line(yearly, x='year', y='positive_rate', markers=True, title="Average Positive Rate per Year")
    return HTMLResponse(fig.to_html(include_plotlyjs='cdn'))

@app.get("/quarterly_chart", response_class=HTMLResponse)
async def quarterly_chart():
    quarterly = load_quarterly_data()
    fig = px.line(
        quarterly, x='quarter',
        y=['new_cases', 'new_deaths', 'new_vaccinations'],
        title="Quarterly COVID Trends",
        markers=True
    )
    return HTMLResponse(fig.to_html(include_plotlyjs='cdn'))

@app.get("/disease_comparison", response_class=HTMLResponse)
async def disease_comparison():
    data = load_combined_disease_data()
    fig = px.line(
        data, x='year', y='count', color='condition', markers=True,
        title="COVID Cases & Vaccinations vs 3 Diseases"
    )
    return HTMLResponse(fig.to_html(include_plotlyjs='cdn'))
