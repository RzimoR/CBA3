
from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import io
import base64

app = FastAPI()

# CORS abilitato per tutti i domini
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

class InputData(BaseModel):
    capex: float
    opex: float
    benefits: float
    years: int
    rate: float  # expressed as percent, e.g., 1.5 means 1.5%

@app.post("/calculate")
def calculate(data: InputData):
    rate_decimal = data.rate / 100.0
    df = pd.DataFrame({
        'Year': list(range(0, data.years + 1)),
        'CAPEX': [data.capex] + [0] * data.years,
        'OPEX': [0] + [data.opex] * data.years,
        'BENEFITS': [0] + [data.benefits] * data.years
    })

    df['discount_factor'] = 1 / (1 + rate_decimal) ** df['Year']
    df['discounted_capex'] = df['CAPEX'] * df['discount_factor']
    df['discounted_opex'] = df['OPEX'] * df['discount_factor']
    df['discounted_benefits'] = df['BENEFITS'] * df['discount_factor']
    df['NPV_year'] = df['discounted_benefits'] - (df['discounted_capex'] + df['discounted_opex'])
    df['NPV_cumulative'] = df['NPV_year'].cumsum()

    total_discounted_costs = df['discounted_capex'].sum() + df['discounted_opex'].sum()
    total_discounted_benefits = df['discounted_benefits'].sum()
    cb_ratio = total_discounted_benefits / total_discounted_costs

    # IRR from raw cash flows
    cash_flows = [-data.capex] + [(data.benefits - data.opex)] * data.years
    irr = np.irr(cash_flows)

    # Plot 1: NPV cumulative
    fig1, ax1 = plt.subplots()
    ax1.plot(df['Year'], df['NPV_cumulative'], marker='o')
    ax1.set_title('Cumulative Net Present Value')
    ax1.set_xlabel('Year')
    ax1.set_ylabel('Cumulative NPV (€)')
    ax1.grid(True)
    fig1.tight_layout()

    buf1 = io.BytesIO()
    fig1.savefig(buf1, format='png')
    buf1.seek(0)
    npv_plot = base64.b64encode(buf1.read()).decode('utf-8')
    plt.close(fig1)

    # Plot 2: Discounted Costs vs Benefits
    fig2, ax2 = plt.subplots()
    width = 0.35
    x = df['Year']
    ax2.bar(x - width/2, df['discounted_benefits'], width, label='Discounted Benefits')
    ax2.bar(x + width/2, df['discounted_capex'] + df['discounted_opex'], width, label='Discounted Costs')
    ax2.set_title('Discounted Costs and Benefits per Year')
    ax2.set_xlabel('Year')
    ax2.set_ylabel('€')
    ax2.legend()
    ax2.grid(True, axis='y')
    fig2.tight_layout()

    buf2 = io.BytesIO()
    fig2.savefig(buf2, format='png')
    buf2.seek(0)
    cost_benefit_plot = base64.b64encode(buf2.read()).decode('utf-8')
    plt.close(fig2)

    return {
        "npv_by_year": df['NPV_year'].round(2).tolist(),
        "npv_cumulative": round(df['NPV_cumulative'].iloc[-1], 2),
        "cb_ratio": round(cb_ratio, 4),
        "irr": round(irr, 4) if irr is not None else None,
        "npv_plot_base64": npv_plot,
        "cost_benefit_plot_base64": cost_benefit_plot
    }
