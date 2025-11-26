# ============================
# Configuración de modelos OpenAI
# ============================

OPENAI_MODELS = {
    "gpt-5.1": {
        "display_name": "GPT 5.1",
        "input_price": 1.25,
        "output_price": 10.00
    },

    "gpt-5-mini": {
        "display_name": "GPT-5 mini",
        "input_price": 0.25,
        "output_price": 2.00
    },

    "gpt-4o": {
        "display_name": "GPT 4o",
        "input_price": 2.50,
        "output_price": 10.00
    },

    "gpt-4.1": {
        "display_name": "GPT 4.1",
        "input_price": 2.00,
        "output_price": 8.00
    },

    "gpt-4.1-mini": {
        "display_name": "GPT-4.1 mini",
        "input_price": 0.40,
        "output_price": 1.60
    },

    "gpt-4.1-nano": {
        "display_name": "GPT-4 nano",
        "input_price": 0.10,
        "output_price": 0.40
    },

    "o4-mini": {
        "display_name": "GPT-o4 mini",
        "input_price": 2.00,
        "output_price": 8.00
    },
}

# Mapa inverso útil: por nombre de display
OPENAI_MODELS_BY_DISPLAY = {
    cfg["display_name"]: key for key, cfg in OPENAI_MODELS.items()
}

# Mapa directo por name del modelo
OPENAI_MODELS_BY_NAME = {
    key: cfg for key, cfg in OPENAI_MODELS.items()
}