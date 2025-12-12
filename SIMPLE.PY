import pandas as pd
import plotly.graph_objects as go

# Read data
print("Loading data...")
health_campaign = pd.read_csv('Health_Campaign_Dataset_50.csv')

# Create  chart - Campaign Performance by Channel
channel_performance = health_campaign.groupby('Channel').agg({
    'Impressions': 'sum',
    'Engagements': 'sum'
}).reset_index()

# Create the chart
fig = go.Figure()
fig.add_trace(go.Bar(
    x=channel_performance['Channel'],
    y=channel_performance['Impressions'],
    name='Impressions',
    marker_color='#3498db'
))
fig.add_trace(go.Bar(
    x=channel_performance['Channel'],
    y=channel_performance['Engagements'],
    name='Engagements',
    marker_color='#e74c3c'
))

fig.update_layout(
    title='Campaign Performance by Channel',
    xaxis_title='Channel',
    yaxis_title='Count',
    barmode='group',
    template='plotly_white',
    height=500
)

# Create simple HTML
html_content = f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Simple Chart</title>
    <script src="https://cdn.plot.ly/plotly-latest.min.js"></script>
    <style>
        body {{
            font-family: Arial, sans-serif;
            margin: 0;
            padding: 20px;
            background: #f5f5f5;
        }}
        .container {{
            max-width: 1200px;
            margin: 0 auto;
            background: white;
            padding: 30px;
            border-radius: 10px;
            box-shadow: 0 2px 10px rgba(0,0,0,0.1);
        }}
        h1 {{
            color: #2c3e50;
            text-align: center;
        }}
    </style>
</head>
<body>
    <div class="container">
        <h1>📊 Campaign Performance Chart</h1>
        {fig.to_html(full_html=False, include_plotlyjs='cdn')}
    </div>
</body>
</html>"""

# Save file
with open('simple_chart.html', 'w', encoding='utf-8') as f:
    f.write(html_content)

print("✅ Simple chart created!")
print("📁 Open: simple_chart.html")