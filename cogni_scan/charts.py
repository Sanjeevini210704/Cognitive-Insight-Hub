import plotly.graph_objects as go
import pandas as pd

PRIMARY = "#7C5CE6"
ACCENT = "#B68BFF"
DESTRUCTIVE = "#E0365F"
CHART_2 = "#6480D8"
CHART_3 = "#1FB5C9"
CHART_4 = "#E37BC4"
CHART_5 = "#F0A05C"
GRID = "rgba(26,27,54,0.08)"
TEXT = "#1A1B36"
MUTED = "#6B7191"
CARD_BG = "rgba(0,0,0,0)"

LAYOUT = dict(
    paper_bgcolor=CARD_BG,
    plot_bgcolor=CARD_BG,
    font=dict(family="Plus Jakarta Sans, sans-serif", color=TEXT, size=12),
    margin=dict(l=20, r=20, t=10, b=20),
    height=320,
    legend=dict(font=dict(color=MUTED, size=11)),
)


def radar_chart(metrics: dict[str, float]):
    cats = list(metrics.keys())
    vals = [metrics[c] * 100 for c in cats]
    fig = go.Figure()
    fig.add_trace(go.Scatterpolar(
        r=vals + [vals[0]], theta=cats + [cats[0]],
        fill="toself", line=dict(color=PRIMARY, width=2),
        fillcolor="rgba(139,93,219,0.35)", name="Score",
    ))
    fig.update_layout(
        **LAYOUT,
        polar=dict(
            bgcolor=CARD_BG,
            radialaxis=dict(visible=True, range=[0, 100], showticklabels=False,
                            gridcolor=GRID, linecolor=GRID),
            angularaxis=dict(gridcolor=GRID, linecolor=GRID,
                             tickfont=dict(color=TEXT, size=11)),
        ),
        showlegend=False,
    )
    return fig


def category_donut(content_breakdown: list[dict]):
    if not content_breakdown:
        content_breakdown = [{"category": "Other", "count": 1}]
    labels = [c["category"] for c in content_breakdown]
    values = [c["count"] for c in content_breakdown]
    palette = [PRIMARY, CHART_3, CHART_2, CHART_4, CHART_5, "#7C3AED",
               "#1FA8D6", "#B85ED0", "#D8784D", "#5070C5"]
    fig = go.Figure(data=[go.Pie(
        labels=labels, values=values, hole=0.62,
        marker=dict(colors=palette[:len(labels)], line=dict(color="#FFFFFF", width=2)),
        textfont=dict(color=TEXT),
    )])
    layout = {**LAYOUT, "legend": dict(orientation="v", x=1.02, y=0.5,
                                       font=dict(color=MUTED, size=11))}
    fig.update_layout(**layout, showlegend=True)
    return fig


def emotional_trend_bar(emotional_trend: list[dict]):
    df = pd.DataFrame(emotional_trend)
    fig = go.Figure()
    fig.add_trace(go.Bar(x=df["day"], y=df["positive"], name="Positive", marker_color=CHART_3))
    fig.add_trace(go.Bar(x=df["day"], y=df["neutral"], name="Neutral", marker_color=CHART_2))
    fig.add_trace(go.Bar(x=df["day"], y=df["negative"], name="Negative", marker_color=DESTRUCTIVE))
    fig.update_layout(**LAYOUT, barmode="stack",
                      xaxis=dict(showgrid=False, color=MUTED, linecolor=GRID),
                      yaxis=dict(gridcolor=GRID, color=MUTED, linecolor=GRID))
    return fig


def engagement_area(engagement_pattern: list[dict]):
    df = pd.DataFrame(engagement_pattern)
    fig = go.Figure()
    fig.add_trace(go.Scatter(
        x=df["hour"], y=df["count"], mode="lines",
        line=dict(color=PRIMARY, width=2),
        fill="tozeroy", fillcolor="rgba(139,93,219,0.25)", name="Posts",
    ))
    fig.update_layout(**LAYOUT,
                      xaxis=dict(dtick=2, gridcolor=GRID, color=MUTED, linecolor=GRID,
                                 title=dict(text="Hour", font=dict(color=MUTED))),
                      yaxis=dict(gridcolor=GRID, color=MUTED, linecolor=GRID))
    return fig


def risk_bar(risk_factors: list[dict]):
    df = pd.DataFrame(risk_factors)
    colors = [DESTRUCTIVE if s >= 7 else ACCENT if s >= 4 else PRIMARY for s in df["severity"]]
    fig = go.Figure(go.Bar(
        x=df["severity"], y=df["factor"], orientation="h",
        marker=dict(color=colors), text=df["severity"], textposition="outside",
        textfont=dict(color=TEXT),
    ))
    fig.update_layout(**LAYOUT,
                      xaxis=dict(range=[0, 10], gridcolor=GRID, color=MUTED, linecolor=GRID),
                      yaxis=dict(autorange="reversed", color=TEXT, linecolor=GRID))
    return fig
