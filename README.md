# UK Dairy Processor Dashboard

A comprehensive environmental monitoring dashboard for UK dairy processors, tracking 270 supplier farms with TNFD-aligned metrics.

## Features

- **Interactive Filters**: Search, region, supplier tier, and risk level filtering
- **Real-time Metrics**: TNFD compliance, average scores, risk assessment
- **Environmental Tracking**: Land, water, and biodiversity metrics
- **Interactive Visualizations**: Regional performance, risk assessment, tier distribution
- **Data Export**: Export farm data for further analysis

## Technology Stack

- **Backend**: Python with Dash framework
- **Data Processing**: Pandas, NumPy
- **Visualization**: Plotly
- **Deployment**: Render (with Gunicorn)

## Local Development

1. Install dependencies:
```bash
pip install -r requirements.txt
```

2. Run the application:
```bash
python app.py
```

3. Open http://localhost:8050 in your browser

## Deployment

This app is configured for deployment on Render. The `render.yaml` file contains all necessary configuration.

## Environment Variables

- `PORT`: Server port (default: 8050)

## Data

The dashboard uses simulated data for 270 UK dairy farms across 8 regions, with various environmental and operational metrics aligned with TNFD requirements.