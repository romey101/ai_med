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


@app.get("/vaccine_line_chart", response_class=HTMLResponse)
async def vaccine_line_chart():
    df = pd.read_csv("app/data/covid_saudi.csv")
    df.columns = df.columns.str.lower().str.strip()
    df = df.sort_values('date')

    df['date'] = pd.to_datetime(df['date'], errors='coerce')
    df['total_cases'] = pd.to_numeric(df['total_cases'], errors='coerce')
    df['total_deaths'] = pd.to_numeric(df['total_deaths'], errors='coerce')
    df['total_vaccinations'] = pd.to_numeric(df['total_vaccinations'], errors='coerce')

    df['new_cases'] = df['total_cases'].diff().fillna(0)
    df['new_deaths'] = df['total_deaths'].diff().fillna(0)

    first_vax_date = df[df['total_vaccinations'] > 0]['date'].min()

    df['period'] = df['date'].apply(lambda d: 'Before Vaccine' if d < first_vax_date else 'After Vaccine')

    import plotly.graph_objects as go
    from plotly.subplots import make_subplots

    fig = make_subplots(rows=1, cols=2, subplot_titles=("New COVID-19 Cases", "New COVID-19 Deaths"))

    for period, color in zip(['Before Vaccine', 'After Vaccine'], ['orange', 'green']):
        data = df[df['period'] == period]
        fig.add_trace(go.Scatter(x=data['date'], y=data['new_cases'], name=f"{period} - Cases", line=dict(color=color)), row=1, col=1)
        fig.add_trace(go.Scatter(x=data['date'], y=data['new_deaths'], name=f"{period} - Deaths", line=dict(color=color)), row=1, col=2)

    fig.add_vline(x=first_vax_date, line=dict(color='gray', dash='dash'), row=1, col=1)
    fig.add_vline(x=first_vax_date, line=dict(color='gray', dash='dash'), row=1, col=2)

    fig.update_layout(
        title_text="COVID-19 Daily Cases & Deaths Before vs After Vaccine",
        showlegend=True,
        height=500
    )

    return HTMLResponse(fig.to_html(include_plotlyjs='cdn'))
