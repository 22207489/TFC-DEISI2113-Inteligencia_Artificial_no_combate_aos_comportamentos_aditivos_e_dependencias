import pandas as pd
import matplotlib.pyplot as plt

# Carregar os dados
df_utentes = pd.read_csv("utentes.csv")


# Filtro: apenas utentes no programa
df_programa = df_utentes[df_utentes['prog_consumo'] == True]

# Contagem dos valores no programa (tratando nulos)
contagem_programa = df_utentes['prog_consumo'].fillna('Não definido').value_counts()
contagem_programa.index = contagem_programa.index.map({True: 'Sim', False: 'Não', 'Não definido': 'Não'})

# Gráfico: No Programa
plt.figure(figsize=(8,6))
ax = contagem_programa.plot(kind='bar', color='mediumseagreen')
plt.title('Número de Utentes no Programa de Acolhimento (SAI)')
plt.xlabel('Está no Programa?')
plt.ylabel('Número de Utentes')
plt.xticks(rotation=0)
plt.grid(axis='y', linestyle='--', alpha=0.7)

# Adicionar valores no topo
for i, v in enumerate(contagem_programa):
    plt.text(i, v + 1, str(v), ha='center', va='bottom', fontsize=9)

plt.tight_layout()
plt.show()

#No Programa-------------------------------------------------------------------------------------------------------

genero_map = {
    1: "Masculino",
    2: "Feminino",
    3: "Transgénero",
    4: "Indefinido"
}

# Mapeamento de concelhos (apenas exemplo inicial — cola o resto ou carrega de ficheiro se quiseres)
concelho_map = {
    1: "Alenquer",
    2: "Amadora",
    3: "Arruda dos Vinhos",
    4: "Azambuja",
    5: "Cadaval",
    6: "Cascais",
    7: "Loures",
    8: "Lourinhã",
    9: "Lx – Belém",
    10: "Lx – Ajuda",
    11: "Lx – Alcântara",
    12: "Lx – Benfica",
    13: "Lx – S. Domingos de Benfica",
    14: "Lx – Alvalade",
    15: "Lx – Marvila",
    16: "Lx – Areeiro",
    17: "Lx – Santo António",
    18: "Lx – Santa Maria Maior",
    19: "Lx – Estrela",
    20: "Lx – Campo de Ourique",
    21: "Lx – Misericórdia",
    22: "Lx – Arroios",
    23: "Lx – Beato",
    24: "Lx – S. Vicente de Fora",
    25: "Lx – Avenidas Novas",
    26: "Lx – Penha de França",
    27: "Lx – Lumiar",
    28: "Lx – Carnide",
    29: "Lx – Santa Clara",
    30: "Lx – Olivais",
    31: "Lx – Campolide",
    32: "Lx – Parque das Nações",
    33: "Mafra",
    34: "Odivelas",
    35: "Oeiras",
    36: "Sintra",
    37: "Sobral de Monte Agraço",
    38: "Torres Vedras",
    39: "Vila Franca de Xira",
    40: "Sem Abrigo",
    41: "Seixal",
    42: "Sem Abrigo",
    43: "Amora",
    44: "Sesimbra",
    45: "Alcobaça",
    46: "Barreiro",
    47: "Palmela",
    48: "Setúbal",
    49: "Cartaxo"
}

# Mapeamento de nacionalidades (exemplo com alguns — usa dicionário completo como tens)
nacionalidade_map = {
    4: "AFEGANISTAO",
    8: "ALBANIA",
    10: "ANTARCTICA",
    12: "ARGELIA",
    16: "SAMOA AMERICANA",
    20: "ANDORRA",
    24: "ANGOLA",
    28: "ANTIGUA E BARBUDA",
    31: "AZERBAIJAO",
    32: "ARGENTINA",
    36: "AUSTRALIA",
    40: "AUSTRIA",
    44: "BAHAMAS",
    48: "BAREM",
    50: "BANGLADESH",
    51: "ARMENIA",
    52: "BARBADOS",
    56: "BELGICA",
    60: "BERMUDA",
    64: "BUTAO",
    68: "BOLIVIA",
    70: "BOSNIA E HERZEGOVINA",
    72: "BOTSWANA",
    74: "ILHAS BOUVET",
    76: "BRASIL",
    84: "BELIZE",
    86: "TERRITORIO BRITANICO DO OCEANO INDICO",
    90: "ILHAS SALOMAO",
    92: "ILHAS VIRGENS (BRITANICAS)",
    96: "BRUNEI DARUSSALAM",
    100: "BULGARIA",
    104: "MYANMAR",
    108: "BURUNDI",
    112: "BIELORRUSSIA",
    116: "CAMBOJA",
    120: "CAMAROES",
    124: "CANADA",
    132: "CABO VERDE",
    136: "ILHAS CAIMAO",
    140: "CENTRO-AFRICANA (REPUBLICA)",
    144: "SRI LANKA",
    148: "CHADE",
    152: "CHILE",
    156: "CHINA",
    158: "TAIWAN",
    162: "ILHAS CHRISTMAS",
    166: "ILHAS COCOS (KEELING)",
    170: "COLOMBIA",
    174: "COMORES",
    175: "MAYOTTE",
    178: "CONGO",
    180: "CONGO (REPUBLICA DEMOCRATICA DO)",
    184: "ILHAS COOK",
    188: "COSTA RICA",
    191: "CROACIA",
    192: "CUBA",
    196: "CHIPRE",
    203: "REPUBLICA CHECA",
    204: "BENIN",
    208: "DINAMARCA",
    212: "DOMINICA",
    214: "REPUBLICA DOMINICANA",
    218: "EQUADOR",
    222: "EL SALVADOR",
    226: "GUINE EQUATORIAL",
    231: "ETIOPIA",
    232: "ERITREIA",
    233: "ESTONIA",
    234: "ILHAS FAROE",
    238: "ILHAS FALKLAND (MALVINAS)",
    239: "GEORGIA DO SUL E ILHAS SANDWICH",
    242: "ILHAS FIJI",
    246: "FINLANDIA",
    248: "ILHAS ALAND",
    250: "FRANCA",
    254: "GUIANA FRANCESA",
    258: "POLINESIA FRANCESA",
    260: "TERRITORIOS FRANCESES DO SUL",
    262: "JIBUTI",
    266: "GABAO",
    268: "GEORGIA",
    270: "GAMBIA",
    275: "TERRITORIO PALESTINIANO OCUPADO",
    276: "ALEMANHA",
    288: "GANA",
    292: "GIBRALTAR",
    296: "KIRIBATI",
    300: "GRECIA",
    304: "GRONELANDIA",
    308: "GRANADA",
    312: "GUADALUPE",
    316: "GUAM",
    320: "GUATEMALA",
    324: "GUINE",
    328: "GUIANA",
    332: "HAITI",
    334: "ILHAS HEARD E ILHAS MCDONALD",
    336: "SANTA SE (CIDADE ESTADO DO VATICANO)",
    340: "HONDURAS",
    344: "HONG KONG",
    348: "HUNGRIA",
    352: "ISLANDIA",
    356: "INDIA",
    360: "INDONESIA",
    364: "IRAO (REPUBLICA ISLAMICA)",
    368: "IRAQUE",
    372: "IRLANDA",
    376: "ISRAEL",
    380: "ITALIA",
    384: "COSTA DO MARFIM",
    388: "JAMAICA",
    392: "JAPAO",
    398: "CAZAQUISTAO",
    400: "JORDANIA",
    404: "KENYA",
    408: "COREIA DO NORTE",
    410: "COREIA (REPUBLICA DA)",
    414: "KUWAIT",
    417: "QUIRGUIZISTAO",
    418: "LAOS (REPUBLICA POPULAR DEMOCRATICA DO)",
    422: "LIBANO",
    426: "LESOTO",
    428: "LETONIA",
    430: "LIBERIA",
    434: "LIBIA (JAMAHIRIYA ARABE DA)",
    438: "LIECHTENSTEIN",
    440: "LITUANIA",
    442: "LUXEMBURGO",
    446: "MACAU",
    450: "MADAGASCAR",
    454: "MALAWI",
    458: "MALASIA",
    462: "MALDIVAS",
    466: "MALI",
    470: "MALTA",
    474: "MARTINICA",
    478: "MAURITANIA",
    480: "MAURICIAS",
    484: "MEXICO",
    492: "MONACO",
    496: "MONGOLIA",
    498: "MOLDOVA (REPUBLICA DE)",
    499: "MONTENEGRO  (REPUBLICA DE)",
    500: "MONSERRATE",
    504: "MARROCOS",
    508: "MOCAMBIQUE",
    512: "OMA",
    516: "NAMIBIA",
    520: "NAURU",
    524: "NEPAL",
    528: "PAISES BAIXOS",
    530: "ANTILHAS HOLANDESAS",
    533: "ARUBA",
    540: "NOVA CALEDONIA",
    548: "VANUATU",
    554: "NOVA ZELANDIA",
    558: "NICARAGUA",
    562: "NIGER",
    566: "NIGERIA",
    570: "NIUE",
    574: "ILHAS NORFOLK",
    578: "NORUEGA",
    580: "ILHAS MARIANAS DO NORTE",
    581: "ILHAS MENORES DISTANTES DOS ESTADOS UNIDOS",
    583: "MICRONESIA (ESTADOS FEDERADOS DA)",
    584: "ILHAS MARSHALL",
    585: "PALAU",
    586: "PAQUISTAO",
    591: "PANAMA",
    598: "PAPUASIA-NOVA GUINE",
    600: "PARAGUAI",
    604: "PERU",
    608: "FILIPINAS",
    612: "PITCAIRN",
    616: "POLONIA",
    620: "PORTUGAL",
    624: "GUINE-BISSAU",
    626: "TIMOR LESTE",
    630: "PORTO RICO",
    634: "CATAR",
    638: "REUNIAO",
    642: "ROMENIA",
    643: "RUSSIA (FEDERACAO DA)",
    646: "RUANDA",
    654: "SANTA HELENA",
    659: "SAO CRISTOVAO E NEVIS",
    660: "ANGUILA",
    662: "SANTA LUCIA",
    666: "SAO PEDRO E MIQUELON",
    670: "SAO VICENTE E GRANADINAS",
    674: "SAO MARINO",
    678: "SAO TOME E PRINCIPE",
    682: "ARABIA SAUDITA",
    686: "SENEGAL",
    688: "SERVIA  (REPUBLICA DA)",
    690: "SEYCHELLES",
    694: "SERRA LEOA",
    702: "SINGAPURA",
    703: "ESLOVACA (REPUBLICA)",
    704: "VIETNAME",
    705: "ESLOVENIA",
    706: "SOMALIA",
    710: "AFRICA DO SUL",
    716: "ZIMBABWE",
    724: "ESPANHA",
    732: "SARA OCIDENTAL",
    736: "SUDAO",
    740: "SURINAME",
    744: "SVALBARD E A ILHA DE JAN MAYEN",
    748: "SUAZILANDIA",
    752: "SUECIA",
    756: "SUICA",
    760: "SIRIA (REPUBLICA ARABE DA)",
    762: "TAJIQUISTAO",
    764: "TAILANDIA",
    768: "TOGO",
    772: "TOKELAU",
    776: "TONGA",
    780: "TRINDADE E TOBAGO",
    784: "EMIRATOS ARABES UNIDOS",
    788: "TUNISIA",
    792: "TURQUIA",
    795: "TURQUEMENISTAO",
    796: "TURCOS E CAICOS (ILHAS)",
    798: "TUVALU",
    800: "UGANDA",
    804: "UCRANIA",
    807: "MACEDONIA (ANTIGA REPUBLICA JUGOSLAVA DA)",
    818: "EGIPTO",
    826: "REINO UNIDO",
    831: "GERNSEY",
    832: "JERSEY",
    833: "ILHA DE MAN",
    834: "TANZANIA, REPUBLICA UNIDA DA",
    840: "ESTADOS UNIDOS",
    850: "ILHAS VIRGENS (ESTADOS UNIDOS)",
    854: "BURKINA FASO",
    858: "URUGUAI",
    860: "USBEQUISTAO",
    862: "VENEZUELA",
    876: "WALLIS E FUTUNA (ILHAS)",
    882: "SAMOA",
    887: "IEMEN",
    891: "SERVIA E MONTENEGRO",
    894: "ZAMBIA",
    895: "DESCONHECIDO",
    1000: "Não atribuido"
}

# Mapear valores
df_programa['genero'] = df_programa['utente_sexo'].map(genero_map)
df_programa['concelho_id'] = df_programa['utente_concelhoresidencia'].map(concelho_map)
df_programa['nacionalidade_id'] = df_programa['utente_nacionalidade'].map(nacionalidade_map)
#Genero---------------------------------------------------------------------------------------------------------
plt.figure(figsize=(8,6))
genero_count = df_programa['genero'].value_counts()
ax = genero_count.plot(kind='bar', color='cornflowerblue')
plt.title('Género dos Utentes no SAI')
plt.xlabel('Género')
plt.ylabel('Número de Utentes')
plt.xticks(rotation=0)
plt.grid(axis='y', linestyle='--', alpha=0.7)
for i, v in enumerate(genero_count):
    plt.text(i, v + 1, str(v), ha='center', va='bottom', fontsize=9)
plt.tight_layout()
plt.show()

# -------------------------------------------------------------------------------------------------------------
# Gráfico: TOP 10 NACIONALIDADES (no programa)
plt.figure(figsize=(10,6))
nac_count = df_programa['nacionalidade_id'].value_counts().head(10)
ax = nac_count.plot(kind='bar', color='seagreen')
plt.title('Principais Países de Origem dos Utentes no SAI')
plt.xlabel('Nacionalidade')
plt.ylabel('Número de Utentes')
plt.xticks(rotation=45, ha='right')
plt.grid(axis='y', linestyle='--', alpha=0.7)
for i, v in enumerate(nac_count):
    plt.text(i, v + 1, str(v), ha='center', va='bottom', fontsize=9)
plt.tight_layout()
plt.show()

# -------------------------------------------------------------------------------------------------------------
# Gráfico: TOP 10 CONCELHOS (no programa)
plt.figure(figsize=(10,6))
conc_count = df_programa['concelho_id'].value_counts().head(10)
ax = conc_count.plot(kind='bar', color='orchid')
plt.title('Concelhos com Maior Número de Utentes no SAI')
plt.xlabel('Concelho')
plt.ylabel('Número de Utentes')
plt.xticks(rotation=45, ha='right')
plt.grid(axis='y', linestyle='--', alpha=0.7)
for i, v in enumerate(conc_count):
    plt.text(i, v + 1, str(v), ha='center', va='bottom', fontsize=9)
plt.tight_layout()
plt.show()