def calcular_distancia(origem, destino, api_key):
    url = "https://maps.googleapis.com/maps/api/directions/json"

    params = {
        "origin": origem,
        "destination": destino,
        "key": api_key,
        "mode": "driving",
        "alternatives": "true",
        "route": "10"
    }

    try:
        response = requests.get(url, params=params)
        response.raise_for_status()

        data = response.json()

        values = []

        for route in data.get('routes', []):
            for leg in route.get('legs', []):
                value = leg.get('distance', {}).get('value')
                if value is not None:
                    values.append(value)

        menor_distancia = min(values) if values else None

        # Verifica se menor_distancia é um número antes de dividir
        if isinstance(menor_distancia, (int, float)):
            return menor_distancia / 1000
        else:
            # Retorna None ou algum outro valor padrão se não for um número
            return None

    except requests.exceptions.RequestException as e:
        st.error(f"Erro na chamada da API: {e}")
        return None
