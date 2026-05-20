# =========================
# CONFIGURAÇÕES GLOBAIS
# =========================

def aplicar_layout(fig):

    fig.update_layout(

        template='plotly_dark',

        height=500,

        margin=dict(
            l=20,
            r=20,
            t=60,
            b=20
        ),

        hovermode='x unified',

        title={
            'x': 0.02,
            'xanchor': 'left'
        },

        legend=dict(
            orientation='h',
            yanchor='bottom',
            y=1.02,
            xanchor='right',
            x=1
        )
    )

    return fig


# =========================
# ESTILO LINHA
# =========================

def estilizar_linha(fig):

    fig.update_traces(
        mode='lines+markers',
        line=dict(width=3),
        marker=dict(size=8)
    )

    return aplicar_layout(fig)


# =========================
# ESTILO BARRAS
# =========================

def estilizar_barra(fig):

    fig.update_traces(
        textposition='outside'
    )

    return aplicar_layout(fig)


# =========================
# ESTILO PIZZA
# =========================

def estilizar_pizza(fig):

    fig.update_traces(
        textinfo='percent+label'
    )

    return aplicar_layout(fig)


# =========================
# ESTILO HEATMAP
# =========================

def estilizar_heatmap(fig):

    return aplicar_layout(fig)
