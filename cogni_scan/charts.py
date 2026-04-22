import plotly.graph_objects as go
import pandas as pd


def radar_chart(metrics: dict[str, float]):
    cats = list(metrics.keys())
    vals = [metrics[c] for c in cats]
    fig = go.Figure()
    fig.add_trace(go.Scatterpolar(r=vals + [vals[0]], theta=cats + [cats[0]],
                                  fill="toself", name="Cognitive Profile",
                                  line=dict(color="#7c3aed")))
    fig.update_layout(polar=dict(radialaxis=dict(visible=True, range=[0, 1])),
                      showlegend=False, title="Cognitive Metrics", height=380)
    return fig


def category_donut(content_breakdown: list[dict]):
    if not content_breakdown:
        content_breakdown = [{"category": "Other", "count": 1}]
    labels = [c["category"] for c in content_breakdown]
    values = [c["count"] for c in content_breakdown]
    fig = go.Figure(data=[go.Pie(labels=labels, values=values, hole=0.55)])
    fig.update_layout(title="Content Category Breakdown", height=380)
    return fig


def emotional_trend_bar(emotional_trend: list[dict]):
    df = pd.DataFrame(emotional_trend)
    fig = go.Figure()
    fig.add_trace(go.Bar(x=df["day"], y=df["positive"], name="Positive", marker_color="#10b981"))
    fig.add_trace(go.Bar(x=df["day"], y=df["neutral"], name="Neutral", marker_color="#9ca3af"))
    fig.add_trace(go.Bar(x=df["day"], y=df["negative"], name="Negative", marker_color="#ef4444"))
    fig.update_layout(barmode="stack", title="Emotional Trend by Day",
                      xaxis_title="Day", yaxis_title="Posts", height=380)
    return fig


def engagement_area(engagement_pattern: list[dict]):
    df = pd.DataFrame(engagement_pattern)
    fig = go.Figure()
    fig.add_trace(go.Scatter(x=df["hour"], y=df["count"], fill="tozeroy",
                             mode="lines", line=dict(color="#0ea5e9"), name="Posts"))
    fig.update_layout(title="Engagement Pattern by Hour",
                      xaxis_title="Hour of Day", yaxis_title="Posts",
                      xaxis=dict(dtick=2), height=380)
    return fig


def risk_bar(risk_factors: list[dict]):
    df = pd.DataFrame(risk_factors)
    fig = go.Figure(go.Bar(x=df["severity"], y=df["factor"], orientation="h",
                           marker_color="#f97316"))
    fig.update_layout(title="Risk Factor Severity (0–10)",
                      xaxis=dict(range=[0, 10]), height=380,
                      yaxis=dict(autorange="reversed"))
    return fig
