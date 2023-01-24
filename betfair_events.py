import datetime
import pandas as pd
import betfairlightweight
import time

username = "tan.olive@bol.com.br"
pw = "@Duda150613"
app_key = "yIfCUygZyO0iXBM2"

# Abrindo a conexão com a lib betfairlightweight
trading = betfairlightweight.APIClient(username, pw, app_key=app_key, cert_files=('./myAppBetfair.crt',
                                                                                  './myAppBetfair.pem'))
x  = trading.login()


# Definindo os filtros de Mercado
filtros_mercado = betfairlightweight.filters.market_filter(
    event_type_ids=['1'],  # ID para Futebol
    competition_ids=[321319],  # Competições
    market_start_time={
        'to': (datetime.datetime.utcnow() + datetime.timedelta(days=1)).strftime("%Y-%m-%dT%TZ")
    }
)

# listando os eventos a partir dos filtros pré definidos acima
eventos_futebol = trading.betting.list_events(
    filter=filtros_mercado
)

# listando as competições de futebol disponíveis
competicoes_futebol = trading.betting.list_competitions(
    filter=filtros_mercado
)

planilha_eventos_futebol = pd.DataFrame({
    'NomeEvento': [obj_evento.event.name for obj_evento in eventos_futebol],
    'IDEvento': [obj_evento.event.id for obj_evento in eventos_futebol],
    'LocalEvento': [obj_evento.event.venue for obj_evento in eventos_futebol],
    'CodPais': [obj_evento.event.country_code for obj_evento in eventos_futebol],
    'TimeZone': [obj_evento.event.time_zone for obj_evento in eventos_futebol],
    'DataAbertura': [obj_evento.event.open_date for obj_evento in eventos_futebol],
    'TotalMercados': [obj_evento.market_count for obj_evento in eventos_futebol],
    'DataLocal': [obj_evento.event.open_date.replace(tzinfo=datetime.timezone.utc).astimezone(tz=None)
                  for obj_evento in eventos_futebol]
})

id_evento = 31065573

filtro_catalogo_mercados = betfairlightweight.filters.market_filter(event_ids=[id_evento])

catalogos_mercado = trading.betting.list_market_catalogue(
    filter=filtro_catalogo_mercados,
    max_results='100',
    sort='FIRST_TO_START',
    market_projection=['RUNNER_METADATA']
)


# Create a DataFrame for each market catalogue
planilha_mercados = pd.DataFrame({
    'NomeMercado': [market_cat_object.market_name for market_cat_object in catalogos_mercado],
    'IDMercado': [market_cat_object.market_id for market_cat_object in catalogos_mercado],
    'TotalCorrespondido': [market_cat_object.total_matched for market_cat_object in catalogos_mercado],
    'Home' : [market_cat_object.runners[0].runner_name for market_cat_object in catalogos_mercado],
    'Home_id' : [market_cat_object.runners[0].selection_id for market_cat_object in catalogos_mercado],
    'Away' : [market_cat_object.runners[1].runner_name for market_cat_object in catalogos_mercado],
    'Away_id' : [market_cat_object.runners[1].selection_id for market_cat_object in catalogos_mercado],
    'Draw' : [market_cat_object.runners[2].runner_name if len(market_cat_object.runners) > 2 else '' for market_cat_object in catalogos_mercado],
    'Draw_id' : [market_cat_object.runners[2].selection_id if len(market_cat_object.runners) > 2 else 0 for market_cat_object in catalogos_mercado]
})


df_final = pd.DataFrame()
for i in range(0,60):
    order_filter = betfairlightweight.filters.ex_best_offers_overrides(
        best_prices_depth=3
    )

    price_filter = betfairlightweight.filters.price_projection(
        price_data=['EX_BEST_OFFERS'],
        ex_best_offers_overrides=order_filter
    )

    # Obtendo odds para o mercado
    market_books = trading.betting.list_market_book(
        market_ids=['1.190674822'],
        price_projection=price_filter
    )
print(eventos_futebol)



