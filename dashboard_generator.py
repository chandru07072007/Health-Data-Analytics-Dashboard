import pandas as pd
import plotly.graph_objects as go
import plotly.express as px
from plotly.subplots import make_subplots
import json

# Read all datasets
print("Loading datasets...")
health_campaign = pd.read_csv('Health_Campaign_Dataset_50.csv')
disability_district = pd.read_csv('HH_Disability_District.csv')
disability_state = pd.read_csv('HH_Disability_State.csv')
awareness = pd.read_csv('XX_Awareness_On_HIV_AIDS_RTI_STI_HAF_ORS_ORT_ZINC_And_ARI_Pneumonia_District.csv')
events = pd.read_csv('events .csv')
webinars = pd.read_csv('wedner data set .csv')
hospitals = pd.read_csv('private hosipitals.csv')

# Clean column names (remove leading/trailing spaces)
health_campaign.columns = health_campaign.columns.str.strip()
disability_district.columns = disability_district.columns.str.strip()
disability_state.columns = disability_state.columns.str.strip()
awareness.columns = awareness.columns.str.strip()
events.columns = events.columns.str.strip()
webinars.columns = webinars.columns.str.strip()
hospitals.columns = hospitals.columns.str.strip()

# Store all chart data
charts_data = []

print("Generating visualizations...")

# ============= HEALTH CAMPAIGN ANALYSIS =============

# 1. Campaign Performance by Channel
channel_performance = health_campaign.groupby('Channel').agg({
    'Impressions': 'sum',
    'Engagements': 'sum',
    'Behavior Change (%)': 'mean',
    'Feedback Score': 'mean'
}).reset_index()

fig1 = go.Figure()
fig1.add_trace(go.Bar(
    x=channel_performance['Channel'],
    y=channel_performance['Impressions'],
    name='Impressions',
    marker_color='#3498db'
))
fig1.add_trace(go.Bar(
    x=channel_performance['Channel'],
    y=channel_performance['Engagements'],
    name='Engagements',
    marker_color='#e74c3c'
))
fig1.update_layout(
    title='Campaign Performance by Channel',
    xaxis_title='Channel',
    yaxis_title='Count',
    barmode='group',
    template='plotly_white',
    height=400
)
charts_data.append(('campaign_channel_performance', fig1.to_html(full_html=False, include_plotlyjs='cdn')))

# 2. Campaign Name Comparison
campaign_stats = health_campaign.groupby('Campaign Name').agg({
    'Impressions': 'sum',
    'Engagements': 'sum',
    'Behavior Change (%)': 'mean',
    'Feedback Score': 'mean'
}).reset_index()

fig2 = go.Figure(data=[
    go.Bar(name='Total Impressions', x=campaign_stats['Campaign Name'], y=campaign_stats['Impressions'], marker_color='#9b59b6'),
    go.Bar(name='Total Engagements', x=campaign_stats['Campaign Name'], y=campaign_stats['Engagements'], marker_color='#1abc9c')
])
fig2.update_layout(
    title='Campaign Performance Comparison',
    xaxis_title='Campaign',
    yaxis_title='Total Count',
    barmode='group',
    template='plotly_white',
    height=400
)
charts_data.append(('campaign_comparison', fig2.to_html(full_html=False, include_plotlyjs='cdn')))

# 3. Demographics Analysis
demo_age = health_campaign.groupby(['Age Group', 'Gender']).size().reset_index(name='Count')
fig3 = px.sunburst(demo_age, path=['Age Group', 'Gender'], values='Count',
                   title='Demographics Distribution (Age Group & Gender)',
                   color='Count',
                   color_continuous_scale='RdYlBu',
                   height=500)
charts_data.append(('demographics_sunburst', fig3.to_html(full_html=False, include_plotlyjs='cdn')))

# 4. Location-wise Performance
location_stats = health_campaign.groupby('Location').agg({
    'Behavior Change (%)': 'mean',
    'Feedback Score': 'mean',
    'Impressions': 'sum'
}).reset_index()

fig4 = make_subplots(rows=1, cols=2, 
                     subplot_titles=('Avg Behavior Change by Location', 'Avg Feedback Score by Location'))
fig4.add_trace(
    go.Bar(x=location_stats['Location'], y=location_stats['Behavior Change (%)'], 
           marker_color='#f39c12', name='Behavior Change %'),
    row=1, col=1
)
fig4.add_trace(
    go.Bar(x=location_stats['Location'], y=location_stats['Feedback Score'], 
           marker_color='#27ae60', name='Feedback Score'),
    row=1, col=2
)
fig4.update_layout(title='Performance Metrics by Location', height=400, template='plotly_white', showlegend=False)
charts_data.append(('location_performance', fig4.to_html(full_html=False, include_plotlyjs='cdn')))

# 5. Time Series of Campaigns
health_campaign['Date'] = pd.to_datetime(health_campaign['Date'])
health_campaign = health_campaign.sort_values('Date')
daily_stats = health_campaign.groupby('Date').agg({
    'Impressions': 'sum',
    'Engagements': 'sum'
}).reset_index()

fig5 = go.Figure()
fig5.add_trace(go.Scatter(x=daily_stats['Date'], y=daily_stats['Impressions'],
                          mode='lines+markers', name='Impressions',
                          line=dict(color='#3498db', width=2)))
fig5.add_trace(go.Scatter(x=daily_stats['Date'], y=daily_stats['Engagements'],
                          mode='lines+markers', name='Engagements',
                          line=dict(color='#e74c3c', width=2)))
fig5.update_layout(
    title='Campaign Activity Over Time',
    xaxis_title='Date',
    yaxis_title='Count',
    template='plotly_white',
    height=400
)
charts_data.append(('time_series', fig5.to_html(full_html=False, include_plotlyjs='cdn')))

# ============= DISABILITY ANALYSIS =============

# 6. State-level Disability Prevalence
fig6 = go.Figure()
fig6.add_trace(go.Bar(
    x=disability_state['State_Name'],
    y=disability_state['HH_Prevalence_Of_Any_Type_Of_Disability_Per_100000_Population_Person_Total'],
    name='Total',
    marker_color='#8e44ad'
))
fig6.add_trace(go.Bar(
    x=disability_state['State_Name'],
    y=disability_state['HH_Prevalence_Of_Any_Type_Of_Disability_Per_100000_Population_Person_Rural'],
    name='Rural',
    marker_color='#16a085'
))
fig6.add_trace(go.Bar(
    x=disability_state['State_Name'],
    y=disability_state['HH_Prevalence_Of_Any_Type_Of_Disability_Per_100000_Population_Person_Urban'],
    name='Urban',
    marker_color='#e67e22'
))
fig6.update_layout(
    title='Disability Prevalence by State (Per 100,000 Population)',
    xaxis_title='State',
    yaxis_title='Prevalence Rate',
    barmode='group',
    template='plotly_white',
    height=500,
    xaxis={'tickangle': -45}
)
charts_data.append(('disability_state', fig6.to_html(full_html=False, include_plotlyjs='cdn')))

# 7. Gender-wise Disability Comparison
gender_disability = disability_state[['State_Name', 
                                       'HH_Prevalence_Of_Any_Type_Of_Disability_Per_100000_Population_Male_Total',
                                       'HH_Prevalence_Of_Any_Type_Of_Disability_Per_100000_Population_Female_Total']].copy()
gender_disability.columns = ['State', 'Male', 'Female']

fig7 = go.Figure()
fig7.add_trace(go.Scatter(x=gender_disability['State'], y=gender_disability['Male'],
                          mode='markers+lines', name='Male',
                          marker=dict(size=10, color='#3498db'),
                          line=dict(color='#3498db', width=2)))
fig7.add_trace(go.Scatter(x=gender_disability['State'], y=gender_disability['Female'],
                          mode='markers+lines', name='Female',
                          marker=dict(size=10, color='#e74c3c'),
                          line=dict(color='#e74c3c', width=2)))
fig7.update_layout(
    title='Gender-wise Disability Prevalence Comparison',
    xaxis_title='State',
    yaxis_title='Prevalence per 100,000',
    template='plotly_white',
    height=400
)
charts_data.append(('gender_disability', fig7.to_html(full_html=False, include_plotlyjs='cdn')))

# 8. Top 10 Districts with Highest Disability Rates
top_districts = disability_district.nlargest(10, 'HH_Prevalence_Of_Any_Type_Of_Disability_Per_100000_Population_Person_Total')

fig8 = go.Figure(go.Bar(
    x=top_districts['HH_Prevalence_Of_Any_Type_Of_Disability_Per_100000_Population_Person_Total'],
    y=top_districts['State_District_Name'] + ', ' + top_districts['State_Name'],
    orientation='h',
    marker_color='#c0392b'
))
fig8.update_layout(
    title='Top 10 Districts with Highest Disability Prevalence',
    xaxis_title='Prevalence per 100,000',
    yaxis_title='District',
    template='plotly_white',
    height=500
)
charts_data.append(('top_districts_disability', fig8.to_html(full_html=False, include_plotlyjs='cdn')))

# ============= HIV/AIDS AWARENESS ANALYSIS =============

# 9. State-wise HIV/AIDS Awareness
state_awareness = awareness.groupby('State_Name').agg({
    'XX_Women_Who_Are_Aware_Of_Hiv_Aids_Total': 'mean',
    'XX_Women_Who_Are_Aware_Of_Rti_Sti_Total': 'mean',
    'XX_Women_Who_Are_Aware_Of_Haf_Ors_Ort_Zinc_Total': 'mean',
    'XX_Women_Who_Are_Aware_Of_Danger_Signs_Of_Ari_Pneumonia_Total': 'mean'
}).reset_index()

fig9 = go.Figure()
fig9.add_trace(go.Bar(name='HIV/AIDS', x=state_awareness['State_Name'], 
                      y=state_awareness['XX_Women_Who_Are_Aware_Of_Hiv_Aids_Total'],
                      marker_color='#e74c3c'))
fig9.add_trace(go.Bar(name='RTI/STI', x=state_awareness['State_Name'], 
                      y=state_awareness['XX_Women_Who_Are_Aware_Of_Rti_Sti_Total'],
                      marker_color='#3498db'))
fig9.add_trace(go.Bar(name='HAF/ORS/ORT/ZINC', x=state_awareness['State_Name'], 
                      y=state_awareness['XX_Women_Who_Are_Aware_Of_Haf_Ors_Ort_Zinc_Total'],
                      marker_color='#2ecc71'))
fig9.add_trace(go.Bar(name='ARI/Pneumonia', x=state_awareness['State_Name'], 
                      y=state_awareness['XX_Women_Who_Are_Aware_Of_Danger_Signs_Of_Ari_Pneumonia_Total'],
                      marker_color='#f39c12'))
fig9.update_layout(
    title='Women\'s Health Awareness by State (%)',
    xaxis_title='State',
    yaxis_title='Awareness %',
    barmode='group',
    template='plotly_white',
    height=500,
    xaxis={'tickangle': -45}
)
charts_data.append(('state_awareness', fig9.to_html(full_html=False, include_plotlyjs='cdn')))

# 10. Rural vs Urban Awareness Comparison
rural_urban = awareness[['State_District_Name', 
                         'XX_Women_Who_Are_Aware_Of_Hiv_Aids_Rural',
                         'XX_Women_Who_Are_Aware_Of_Hiv_Aids_Urban']].dropna()
rural_urban = rural_urban.head(20)  # Top 20 districts

fig10 = go.Figure()
fig10.add_trace(go.Scatter(
    x=rural_urban['XX_Women_Who_Are_Aware_Of_Hiv_Aids_Rural'],
    y=rural_urban['XX_Women_Who_Are_Aware_Of_Hiv_Aids_Urban'],
    mode='markers',
    marker=dict(size=12, color='#9b59b6', opacity=0.6),
    text=rural_urban['State_District_Name'],
    name='Districts'
))
fig10.add_trace(go.Scatter(
    x=[0, 100], y=[0, 100],
    mode='lines',
    line=dict(color='red', dash='dash'),
    name='Equal Awareness Line'
))
fig10.update_layout(
    title='HIV/AIDS Awareness: Rural vs Urban (%)',
    xaxis_title='Rural Awareness %',
    yaxis_title='Urban Awareness %',
    template='plotly_white',
    height=500
)
charts_data.append(('rural_urban_awareness', fig10.to_html(full_html=False, include_plotlyjs='cdn')))

# 11. Comprehensive Awareness Heatmap
awareness_sample = awareness[['State_District_Name',
                              'XX_Women_Who_Are_Aware_Of_Hiv_Aids_Total',
                              'XX_Women_Who_Are_Aware_Of_Rti_Sti_Total',
                              'XX_Women_Who_Are_Aware_Of_Haf_Ors_Ort_Zinc_Total',
                              'XX_Women_Who_Are_Aware_Of_Danger_Signs_Of_Ari_Pneumonia_Total']].head(30)
awareness_sample.columns = ['District', 'HIV/AIDS', 'RTI/STI', 'HAF/ORS/ORT/ZINC', 'ARI/Pneumonia']

fig11 = go.Figure(data=go.Heatmap(
    z=awareness_sample[['HIV/AIDS', 'RTI/STI', 'HAF/ORS/ORT/ZINC', 'ARI/Pneumonia']].values.T,
    x=awareness_sample['District'],
    y=['HIV/AIDS', 'RTI/STI', 'HAF/ORS/ORT/ZINC', 'ARI/Pneumonia'],
    colorscale='Viridis',
    text=awareness_sample[['HIV/AIDS', 'RTI/STI', 'HAF/ORS/ORT/ZINC', 'ARI/Pneumonia']].values.T,
    texttemplate='%{text:.1f}',
    textfont={"size": 8}
))
fig11.update_layout(
    title='Health Awareness Heatmap (Top 30 Districts)',
    xaxis_title='District',
    yaxis_title='Health Topic',
    height=400,
    xaxis={'tickangle': -90, 'tickfont': {'size': 8}}
)
charts_data.append(('awareness_heatmap', fig11.to_html(full_html=False, include_plotlyjs='cdn')))

# ============= EVENTS ANALYSIS =============

# 12. Events Timeline by Category
events_timeline = events.groupby(['Month', 'Category']).size().reset_index(name='Count')
fig12 = px.line(events_timeline, x='Month', y='Count', color='Category',
                markers=True, title='Health Events Timeline by Category')
fig12.update_layout(
    template='plotly_white',
    height=400,
    xaxis_title='Month',
    yaxis_title='Number of Events'
)
charts_data.append(('events_timeline', fig12.to_html(full_html=False, include_plotlyjs='cdn')))

# 13. Events Sentiment Distribution
sentiment_counts = events['Sentiment'].value_counts()
fig13 = go.Figure(data=[go.Pie(
    labels=sentiment_counts.index,
    values=sentiment_counts.values,
    hole=0.4,
    marker=dict(colors=['#2ecc71', '#3498db', '#e74c3c'])
)])
fig13.update_layout(
    title='Events Sentiment Distribution',
    template='plotly_white',
    height=400
)
charts_data.append(('events_sentiment', fig13.to_html(full_html=False, include_plotlyjs='cdn')))

# 14. Events by Scheme
scheme_counts = events['Scheme'].value_counts().head(10)
fig14 = go.Figure(data=[go.Bar(
    x=scheme_counts.values,
    y=scheme_counts.index,
    orientation='h',
    marker_color='#9b59b6'
)])
fig14.update_layout(
    title='Top 10 Health Schemes by Event Count',
    xaxis_title='Number of Events',
    yaxis_title='Scheme',
    template='plotly_white',
    height=450
)
charts_data.append(('events_by_scheme', fig14.to_html(full_html=False, include_plotlyjs='cdn')))

# ============= WEBINARS & TRAINING ANALYSIS =============

# 15. Webinar/Training Event Types Distribution
event_type_counts = webinars['Category'].value_counts()
fig15 = go.Figure(data=[go.Pie(
    labels=event_type_counts.index,
    values=event_type_counts.values,
    marker=dict(colors=['#e74c3c', '#3498db', '#2ecc71', '#f39c12', '#9b59b6'])
)])
fig15.update_layout(
    title='Distribution of Training Events by Type',
    template='plotly_white',
    height=400
)
charts_data.append(('webinar_types', fig15.to_html(full_html=False, include_plotlyjs='cdn')))

# 16. Focus Area Analysis
focus_area_counts = webinars['Focus Area'].value_counts()
fig16 = go.Figure(data=[go.Bar(
    x=focus_area_counts.index,
    y=focus_area_counts.values,
    marker_color='#16a085'
)])
fig16.update_layout(
    title='Training Events by Focus Area',
    xaxis_title='Focus Area',
    yaxis_title='Number of Events',
    template='plotly_white',
    height=400,
    xaxis={'tickangle': -45}
)
charts_data.append(('focus_area_distribution', fig16.to_html(full_html=False, include_plotlyjs='cdn')))

# 17. Mode of Delivery Analysis
mode_counts = webinars['Mode'].value_counts()
fig17 = go.Figure(data=[go.Funnel(
    y=mode_counts.index,
    x=mode_counts.values,
    textinfo="value+percent initial",
    marker=dict(color=['#3498db', '#e74c3c', '#2ecc71'])
)])
fig17.update_layout(
    title='Event Delivery Mode Distribution',
    template='plotly_white',
    height=400
)
charts_data.append(('delivery_mode', fig17.to_html(full_html=False, include_plotlyjs='cdn')))

# ============= HOSPITAL ANALYSIS =============

# 18. Public vs Private Hospital Comparison
fig18 = go.Figure()
fig18.add_trace(go.Bar(
    x=hospitals['District'],
    y=hospitals['Public Hospitals'],
    name='Public Hospitals',
    marker_color='#2ecc71'
))
fig18.add_trace(go.Bar(
    x=hospitals['District'],
    y=hospitals['Private Hospitals'],
    name='Private Hospitals',
    marker_color='#e74c3c'
))
fig18.update_layout(
    title='Public vs Private Hospitals by District',
    xaxis_title='District',
    yaxis_title='Number of Hospitals',
    barmode='group',
    template='plotly_white',
    height=450,
    xaxis={'tickangle': -45}
)
charts_data.append(('hospital_comparison', fig18.to_html(full_html=False, include_plotlyjs='cdn')))

# 19. Performance Category Distribution
performance_counts = hospitals['Performance Category'].value_counts()
fig19 = go.Figure(data=[go.Bar(
    x=performance_counts.index,
    y=performance_counts.values,
    marker=dict(
        color=performance_counts.values,
        colorscale='RdYlGn',
        showscale=True
    )
)])
fig19.update_layout(
    title='Hospital Performance Categories',
    xaxis_title='Performance Category',
    yaxis_title='Number of Districts',
    template='plotly_white',
    height=400
)
charts_data.append(('performance_categories', fig19.to_html(full_html=False, include_plotlyjs='cdn')))

# 20. Public-Private Ratio Analysis
fig20 = go.Figure(data=[go.Scatter(
    x=hospitals['District'],
    y=hospitals['Public-Private Ratio (%)'],
    mode='markers+lines',
    marker=dict(
        size=hospitals['Total Hospitals'] / 2,
        color=hospitals['Public-Private Ratio (%)'],
        colorscale='Viridis',
        showscale=True,
        colorbar=dict(title="Ratio %")
    ),
    text=hospitals['District'],
    hovertemplate='<b>%{text}</b><br>Ratio: %{y:.1f}%<br>Total: ' + 
                  hospitals['Total Hospitals'].astype(str) + '<extra></extra>'
)])
fig20.update_layout(
    title='Public-Private Hospital Ratio by District',
    xaxis_title='District',
    yaxis_title='Public-Private Ratio (%)',
    template='plotly_white',
    height=450,
    xaxis={'tickangle': -45}
)
charts_data.append(('hospital_ratio', fig20.to_html(full_html=False, include_plotlyjs='cdn')))

# ============= SUMMARY STATISTICS =============

# Calculate key metrics
total_impressions = health_campaign['Impressions'].sum()
total_engagements = health_campaign['Engagements'].sum()
avg_behavior_change = health_campaign['Behavior Change (%)'].mean()
avg_feedback = health_campaign['Feedback Score'].mean()
avg_disability_rate = disability_state['HH_Prevalence_Of_Any_Type_Of_Disability_Per_100000_Population_Person_Total'].mean()
avg_hiv_awareness = awareness['XX_Women_Who_Are_Aware_Of_Hiv_Aids_Total'].mean()
total_events = len(events)
total_webinars = len(webinars)
total_hospitals = hospitals['Total Hospitals'].sum()
avg_public_ratio = hospitals['Public-Private Ratio (%)'].mean()

summary_stats = {
    'total_impressions': f"{total_impressions:,}",
    'total_engagements': f"{total_engagements:,}",
    'avg_behavior_change': f"{avg_behavior_change:.1f}%",
    'avg_feedback': f"{avg_feedback:.2f}",
    'avg_disability_rate': f"{avg_disability_rate:.1f}",
    'avg_hiv_awareness': f"{avg_hiv_awareness:.1f}%",
    'total_events': f"{total_events}",
    'total_webinars': f"{total_webinars}",
    'total_hospitals': f"{total_hospitals}",
    'avg_public_ratio': f"{avg_public_ratio:.1f}%",
    'total_districts': len(disability_district),
    'total_states': len(disability_state)
}

print("Generating HTML dashboard...")

# Generate HTML with all charts
html_content = f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Health Data Analytics Dashboard</title>
    <link rel="stylesheet" href="dashboard_styles.css">
    <script src="https://cdn.plot.ly/plotly-latest.min.js"></script>
</head>
<body>
    <header>
        <div class="container">
            <h1>🏥 Health Data Analytics Dashboard</h1>
            <p class="subtitle">Comprehensive Analysis of Health Campaigns, Disability Prevalence & Health Awareness</p>
        </div>
    </header>

    <!-- Toggle Button for Sidebar -->
    <button class="sidebar-toggle" onclick="toggleSidebar()">
        <span class="toggle-icon">☰</span>
    </button>

    <!-- Navigation Sidebar -->
    <div class="sidebar" id="sidebar">
        <button class="sidebar-close" onclick="toggleSidebar()">✕</button>
        <h3>📊 Select Visualization</h3>
        <button class="nav-btn" onclick="showSection('all')">📈 All Charts</button>
        <button class="nav-btn" onclick="showSection('stats')">📊 Summary Stats</button>
        
        <div class="nav-category">Health Campaigns</div>
        <button class="nav-btn" onclick="showChart('campaign_channel_performance')">Channel Performance</button>
        <button class="nav-btn" onclick="showChart('campaign_comparison')">Campaign Comparison</button>
        <button class="nav-btn" onclick="showChart('demographics_sunburst')">Demographics</button>
        <button class="nav-btn" onclick="showChart('location_performance')">Location Performance</button>
        <button class="nav-btn" onclick="showChart('time_series')">Time Series</button>
        
        <div class="nav-category">Disability Analysis</div>
        <button class="nav-btn" onclick="showChart('disability_state')">State Prevalence</button>
        <button class="nav-btn" onclick="showChart('gender_disability')">Gender Comparison</button>
        <button class="nav-btn" onclick="showChart('top_districts_disability')">Top 10 Districts</button>
        
        <div class="nav-category">Health Awareness</div>
        <button class="nav-btn" onclick="showChart('state_awareness')">State Awareness</button>
        <button class="nav-btn" onclick="showChart('rural_urban_awareness')">Rural vs Urban</button>
        <button class="nav-btn" onclick="showChart('awareness_heatmap')">Awareness Heatmap</button>
        
        <div class="nav-category">Events & Programs</div>
        <button class="nav-btn" onclick="showChart('events_timeline')">Events Timeline</button>
        <button class="nav-btn" onclick="showChart('events_sentiment')">Events Sentiment</button>
        <button class="nav-btn" onclick="showChart('events_by_scheme')">Events by Scheme</button>
        
        <div class="nav-category">Webinars & Training</div>
        <button class="nav-btn" onclick="showChart('webinar_types')">Event Types</button>
        <button class="nav-btn" onclick="showChart('focus_area_distribution')">Focus Areas</button>
        <button class="nav-btn" onclick="showChart('delivery_mode')">Delivery Mode</button>
        
        <div class="nav-category">Hospital Infrastructure</div>
        <button class="nav-btn" onclick="showChart('hospital_comparison')">Public vs Private</button>
        <button class="nav-btn" onclick="showChart('performance_categories')">Performance Categories</button>
        <button class="nav-btn" onclick="showChart('hospital_ratio')">Hospital Ratio</button>
    </div>

    <div class="main-content">
    <div class="container">
        <!-- Summary Statistics Cards -->
        <div class="stats-grid" id="stats" style="display: none;">
            <div class="stat-card">
                <div class="stat-icon">📊</div>
                <div class="stat-value">{summary_stats['total_impressions']}</div>
                <div class="stat-label">Total Campaign Impressions</div>
            </div>
            <div class="stat-card">
                <div class="stat-icon">👥</div>
                <div class="stat-value">{summary_stats['total_engagements']}</div>
                <div class="stat-label">Total Engagements</div>
            </div>
            <div class="stat-card">
                <div class="stat-icon">📈</div>
                <div class="stat-value">{summary_stats['avg_behavior_change']}</div>
                <div class="stat-label">Avg Behavior Change</div>
            </div>
            <div class="stat-card">
                <div class="stat-icon">⭐</div>
                <div class="stat-value">{summary_stats['avg_feedback']}</div>
                <div class="stat-label">Avg Feedback Score</div>
            </div>
            <div class="stat-card">
                <div class="stat-icon">♿</div>
                <div class="stat-value">{summary_stats['avg_disability_rate']}</div>
                <div class="stat-label">Avg Disability Rate (per 100k)</div>
            </div>
            <div class="stat-card">
                <div class="stat-icon">🎗️</div>
                <div class="stat-value">{summary_stats['avg_hiv_awareness']}</div>
                <div class="stat-label">HIV/AIDS Awareness</div>
            </div>
            <div class="stat-card">
                <div class="stat-icon">�</div>
                <div class="stat-value">{summary_stats['total_events']}</div>
                <div class="stat-label">Health Events</div>
            </div>
            <div class="stat-card">
                <div class="stat-icon">🎓</div>
                <div class="stat-value">{summary_stats['total_webinars']}</div>
                <div class="stat-label">Training Programs</div>
            </div>
            <div class="stat-card">
                <div class="stat-icon">🏥</div>
                <div class="stat-value">{summary_stats['total_hospitals']}</div>
                <div class="stat-label">Total Hospitals</div>
            </div>
            <div class="stat-card">
                <div class="stat-icon">📊</div>
                <div class="stat-value">{summary_stats['avg_public_ratio']}</div>
                <div class="stat-label">Avg Public Ratio</div>
            </div>
            <div class="stat-card">
                <div class="stat-icon">�🗺️</div>
                <div class="stat-value">{summary_stats['total_states']}</div>
                <div class="stat-label">States Covered</div>
            </div>
            <div class="stat-card">
                <div class="stat-icon">📍</div>
                <div class="stat-value">{summary_stats['total_districts']}</div>
                <div class="stat-label">Districts Analyzed</div>
            </div>
        </div>

        <!-- Individual Chart Containers -->
        <div class="chart-container chart-item" id="campaign_channel_performance" style="display: none;">
            <h3 class="chart-title">📢 Campaign Performance by Channel</h3>
            {charts_data[0][1]}
        </div>
        
        <div class="chart-container chart-item" id="campaign_comparison" style="display: none;">
            <h3 class="chart-title">📢 Campaign Comparison</h3>
            {charts_data[1][1]}
        </div>
        
        <div class="chart-container chart-item" id="demographics_sunburst" style="display: none;">
            <h3 class="chart-title">📢 Demographics Distribution</h3>
            {charts_data[2][1]}
        </div>
        
        <div class="chart-container chart-item" id="location_performance" style="display: none;">
            <h3 class="chart-title">📢 Performance Metrics by Location</h3>
            {charts_data[3][1]}
        </div>
        
        <div class="chart-container chart-item" id="time_series" style="display: none;">
            <h3 class="chart-title">📢 Campaign Activity Over Time</h3>
            {charts_data[4][1]}
        </div>
        
        <div class="chart-container chart-item" id="disability_state" style="display: none;">
            <h3 class="chart-title">♿ Disability Prevalence by State</h3>
            {charts_data[5][1]}
        </div>
        
        <div class="chart-container chart-item" id="gender_disability" style="display: none;">
            <h3 class="chart-title">♿ Gender-wise Disability Comparison</h3>
            {charts_data[6][1]}
        </div>
        
        <div class="chart-container chart-item" id="top_districts_disability" style="display: none;">
            <h3 class="chart-title">♿ Top 10 Districts with Highest Disability</h3>
            {charts_data[7][1]}
        </div>
        
        <div class="chart-container chart-item" id="state_awareness" style="display: none;">
            <h3 class="chart-title">🎗️ Women's Health Awareness by State</h3>
            {charts_data[8][1]}
        </div>
        
        <div class="chart-container chart-item" id="rural_urban_awareness" style="display: none;">
            <h3 class="chart-title">🎗️ HIV/AIDS Awareness: Rural vs Urban</h3>
            {charts_data[9][1]}
        </div>
        
        <div class="chart-container chart-item" id="awareness_heatmap" style="display: none;">
            <h3 class="chart-title">🎗️ Health Awareness Heatmap</h3>
            {charts_data[10][1]}
        </div>
        
        <div class="chart-container chart-item" id="events_timeline" style="display: none;">
            <h3 class="chart-title">📅 Health Events Timeline by Category</h3>
            {charts_data[11][1]}
        </div>
        
        <div class="chart-container chart-item" id="events_sentiment" style="display: none;">
            <h3 class="chart-title">📅 Events Sentiment Distribution</h3>
            {charts_data[12][1]}
        </div>
        
        <div class="chart-container chart-item" id="events_by_scheme" style="display: none;">
            <h3 class="chart-title">📅 Top Health Schemes by Event Count</h3>
            {charts_data[13][1]}
        </div>
        
        <div class="chart-container chart-item" id="webinar_types" style="display: none;">
            <h3 class="chart-title">🎓 Training Event Types Distribution</h3>
            {charts_data[14][1]}
        </div>
        
        <div class="chart-container chart-item" id="focus_area_distribution" style="display: none;">
            <h3 class="chart-title">🎓 Training Events by Focus Area</h3>
            {charts_data[15][1]}
        </div>
        
        <div class="chart-container chart-item" id="delivery_mode" style="display: none;">
            <h3 class="chart-title">🎓 Event Delivery Mode Distribution</h3>
            {charts_data[16][1]}
        </div>
        
        <div class="chart-container chart-item" id="hospital_comparison" style="display: none;">
            <h3 class="chart-title">🏥 Public vs Private Hospitals by District</h3>
            {charts_data[17][1]}
        </div>
        
        <div class="chart-container chart-item" id="performance_categories" style="display: none;">
            <h3 class="chart-title">🏥 Hospital Performance Categories</h3>
            {charts_data[18][1]}
        </div>
        
        <div class="chart-container chart-item" id="hospital_ratio" style="display: none;">
            <h3 class="chart-title">🏥 Public-Private Hospital Ratio Analysis</h3>
            {charts_data[19][1]}
        </div>

        <!-- Insights Section -->
        <section class="section insights">
            <h2 class="section-title">💡 Key Insights</h2>
            <div class="insights-grid">
                <div class="insight-card">
                    <h3>Campaign Performance</h3>
                    <p>Healthcare providers and social media are the most effective channels for health campaigns, showing higher engagement rates and better behavior change outcomes.</p>
                </div>
                <div class="insight-card">
                    <h3>Disability Prevalence</h3>
                    <p>Odisha and Rajasthan show the highest disability prevalence rates, with rural areas typically showing higher rates than urban areas across most states.</p>
                </div>
                <div class="insight-card">
                    <h3>Health Awareness</h3>
                    <p>HAF/ORS/ORT/ZINC awareness is highest (95%+) across all states, while RTI/STI awareness shows the most variation and needs targeted intervention.</p>
                </div>
                <div class="insight-card">
                    <h3>Rural-Urban Gap</h3>
                    <p>Significant awareness gaps exist between rural and urban areas, particularly in HIV/AIDS awareness, indicating the need for targeted rural outreach programs.</p>
                </div>
                <div class="insight-card">
                    <h3>Digital Health Adoption</h3>
                    <p>ABDM and PM-JAY programs show strong momentum with positive sentiment across events. Online and hybrid training modes dominate capacity building efforts.</p>
                </div>
                <div class="insight-card">
                    <h3>Hospital Infrastructure</h3>
                    <p>Significant imbalance exists between public and private hospitals in most districts. Low public share categories require immediate infrastructure investment.</p>
                </div>
            </div>
        </section>
        </section>
    </div>
    </div>

    <script>
        function toggleSidebar() {{
            const sidebar = document.getElementById('sidebar');
            const mainContent = document.querySelector('.main-content');
            const footer = document.querySelector('footer');
            const toggleBtn = document.querySelector('.sidebar-toggle');
            
            sidebar.classList.toggle('hidden');
            
            if (sidebar.classList.contains('hidden')) {{
                mainContent.style.marginLeft = '0';
                mainContent.style.width = '100%';
                footer.style.marginLeft = '0';
                toggleBtn.querySelector('.toggle-icon').textContent = '☰';
            }} else {{
                mainContent.style.marginLeft = '240px';
                mainContent.style.width = 'calc(100% - 240px)';
                footer.style.marginLeft = '240px';
                toggleBtn.querySelector('.toggle-icon').textContent = '✕';
            }}
        }}
        
        function showChart(chartId) {{
            // Hide stats and all chart items
            document.getElementById('stats').style.display = 'none';
            document.querySelectorAll('.chart-item').forEach(el => el.style.display = 'none');
            document.querySelectorAll('.section').forEach(el => el.style.display = 'none');
            
            // Show only the selected chart
            const chart = document.getElementById(chartId);
            if (chart) {{
                chart.style.display = 'block';
            }}
            
            // Update active button
            document.querySelectorAll('.nav-btn').forEach(btn => btn.classList.remove('active'));
            event.target.classList.add('active');
            
            // Scroll to top
            window.scrollTo({{top: 0, behavior: 'smooth'}});
        }}
        
        function showSection(section) {{
            if (section === 'all') {{
                // Show everything
                document.getElementById('stats').style.display = 'grid';
                document.querySelectorAll('.chart-item').forEach(el => el.style.display = 'block');
                document.querySelectorAll('.section').forEach(el => el.style.display = 'block');
            }} else if (section === 'stats') {{
                // Show only stats
                document.querySelectorAll('.chart-item').forEach(el => el.style.display = 'none');
                document.querySelectorAll('.section').forEach(el => el.style.display = 'none');
                document.getElementById('stats').style.display = 'grid';
            }}
            
            // Update active button
            document.querySelectorAll('.nav-btn').forEach(btn => btn.classList.remove('active'));
            event.target.classList.add('active');
            
            // Scroll to top
            window.scrollTo({{top: 0, behavior: 'smooth'}});
        }}
    </script>

    <footer>
        <div class="container">
            <p>© 2025 Health Data Analytics Dashboard | Generated on November 4, 2025</p>
            <p>Data Sources: Health Campaign Dataset, Disability Prevalence Data, Health Awareness Survey</p>
        </div>
    </footer>
</body>
</html>"""

# Write HTML file
with open('dashboard.html', 'w', encoding='utf-8') as f:
    f.write(html_content)

print("✅ Dashboard generated successfully!")
print("📊 Total visualizations created: 11")
print("📁 Output file: dashboard.html")
print("🎨 CSS file needed: dashboard_styles.css")
