# Data retrieval via  API from https://api.raporty.pse.pl/

import requests
import datetime
from datetime import timedelta
import json
import pandas as pd
import pprint

from dash import Dash, html, dcc, callback, Output, Input
import plotly.express as px
import plotly.graph_objects as go
import dash_bootstrap_components as dbc

# data explenation

# Doba i godzina: udtczas
# Planowane saldo wymiany międzysystemowej: swm_pbm_p_ow
# Doba handlowa: business_date
# Nadwyżka mocy dostępna dla OSP: kse_pbm_rez_d
# Wymagana rezerwa mocy OSP: kse_pbm_wrm_d
# Data publikacji: source_datetime
# Obowiązki mocowe wszystkich jednostek rynku mocy: s_jrm_pbm_sum_om
# Przewidywana generacja zasobów wytwórczych nieobjętych obowiązkami mocowymi: s_njrm_pbm_p_gen
# Nadwyżka mocy dostępna dla OSP ponad wymaganą rezerwę mocy: kse_pbm_nad_wrm_d
# Prognozowana generacja JW i magazynów energii nie świadczących usług bilansujących w ramach RB: s_nrb_pbm_p_gen_si
# Prognozowana sumaryczna generacja źródeł fotowoltaicznych: s_pv_pbm_p_gen_prg
# Prognozowana sumaryczna generacja źródeł wiatrowych: s_wi_pbm_p_gen_prg
# Prognozowane zapotrzebowanie sieci: zap_pokr_pbm_zap_s
# Przewidywana generacja JW i magazynów energii świadczących usługi bilansujące w ramach RB: zap_pokr_pbm_zap_pok_n
# Suma niedostępności (postoje + ubytki) ze względu na warunki eksploatacyjne (WE): s_jg_a_w1_pbm_sum_up_el_we_gen
# Prognozowana wielkość niedyspozycyjności wynikająca z ograniczeń sieciowych występujących w sieci przesyłowej oraz sieci dystrybucyjnej w zakresie dostarczania energii elektrycznej: s_jg_a_w1m1z1_pbm_sum_up_si_gen
# Planowane ograniczenia dyspozycyjności i odstawień MWE: _mwe_110plus_pbm_sum_up_el_gen
# Moc dyspozycyjna JW i magazynów energii świadczących usługi bilansujące w ramach RB: s_jg_a_wm_pbm_p_dysp_max_ruch_gen
# Moc dyspozycyjna JW i magazynów energii świadczących usługi bilansujące w ramach RB dostępna dla OSP: s_jg_a_wm_pbm_p_dysp_max_ruch_zw_gen

# dates for chart
current_date = datetime.datetime.now()
custom_time = current_date.replace(hour=0, minute=0, second=0, microsecond=0)  #current day from 00:00:00
start_date = custom_time.strftime('%Y-%m-%d %H:%M:%S')

future_datetime = custom_time + timedelta(hours=95)
end_date = future_datetime.strftime("%Y-%m-%d %H:%M:%S")

response = requests.get(f"https://api.raporty.pse.pl/api/pk5l-wp?$filter=udtczas ge '{start_date}' and udtczas le '{end_date}'&$select=udtczas,swm_pbm_p_ow,kse_pbm_rez_d,kse_pbm_wrm_d,source_datetime,s_pv_pbm_p_gen_prg,s_wi_pbm_p_gen_prg,zap_pokr_pbm_zap_s")

if response.status_code == 200:
    print("Data successfully got!")
else:
    print(f"Failed to get data. Status code: {response.status_code}")

# Covert response to JSON
payload = response.json()

pp = pprint.PrettyPrinter(indent=1)
#pp.pprint(payload)

# Get only values from JSON
data = payload['value']

# Data Frame
df = pd.DataFrame(data)
#print(df)

# write JSON to a file
json_object = json.dumps(data, indent=4)

#with open("KSE_data.json", "w") as outfile:
#    outfile.write(json_object)



# data preparation
df=df.rename(columns={'udtczas':'time',
                      'swm_pbm_p_ow':'exchange',
                      'kse_pbm_rez_d':'reserve',
                      'kse_pbm_wrm_d':'required_reserve',
                      's_pv_pbm_p_gen_prg':'pv',
                      's_wi_pbm_p_gen_prg':'wind',
                      'zap_pokr_pbm_zap_s':'demand'
                        })


print(df)

