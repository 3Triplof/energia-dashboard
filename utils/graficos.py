import plotly.io as pio

pio.templates.default = "plotly_dark"


def aplicar_layout(fig, height=500, template="plotly_dark", showlegend=True):
    fig.update_layout(
        template=template,
        height=height,
        margin=dict(l=20, r=20, t=60, b=20),
        hovermode="x unified",
        title=dict(x=0.02, xanchor="left"),
        legend=dict(
            orientation="h",
            yanchor="bottom",
            y=1.02,
            xanchor="right",
            x=1
        ),
        showlegend=showlegend
    )
    return fig


def estilizar_linha(fig):
    fig.update_traces(
        mode="lines+markers",
        line=dict(width=3),
        marker=dict(size=8)
    )
    return aplicar_layout(fig)


def estilizar_barra(fig):
    fig.update_traces(
        textposition="outside",
        cliponaxis=False
    )
    return aplicar_layout(fig)


def estilizar_pizza(fig, donut=False):
    if donut:
        fig.update_traces(
            textinfo="percent+label",
            hole=0.45
        )
    else:
        fig.update_traces(
            textinfo="percent+label"
        )
    return aplicar_layout(fig, showlegend=True)


def estilizar_heatmap(fig):
    fig.update_layout(
        coloraxis_colorbar=dict(title="Consumo")
    )
    return aplicar_layout(fig)
