# Monitoramento climático

Projeto de dados que consulta condições meteorológicas na API
Open-Meteo, armazena observações em SQLite e apresenta os
indicadores em um dashboard no Tableau Public.

## Dashboard

[Acesse o painel interativo](https://public.tableau.com/app/profile/thiago.betone2350/viz/MonitoramentoClimtico/MonitoramentoClimtico)

O painel apresenta temperatura, sensação térmica, umidade e
velocidade do vento da última observação disponível por cidade.

## Fluxo dos dados

API Open-Meteo → Python → SQLite → CSV → Tableau Public

## Funcionalidades

- Consulta das condições meteorológicas por coordenadas.
- Armazenamento do histórico por cidade.
- Atualização de registros sem duplicar cidade e horário.
- Exportação dos dados para CSV.
- Dashboard com filtro por cidade.
- Testes automatizados da API, banco e serviço de coleta.

## Como executar

Desenvolvido com Python 3.14.7. Os comandos abaixo são para
PowerShell no Windows.

### Preparar o ambiente

```powershell
git clone https://github.com/ThiagoBetone/monitoramento-climatico.git
cd monitoramento-climatico
python -m venv .venv
.\.venv\Scripts\python.exe -m pip install -r requirements.txt
```

### Coletar e exportar os dados

```powershell
.\.venv\Scripts\python.exe main.py
.\.venv\Scripts\python.exe export_csv.py
```

O primeiro comando consulta a API e salva a observação no SQLite.

Atualmente, a coleta está configurada para Assis (SP).
Para consultar outra cidade, altere o nome, a latitude e a longitude na
chamada collect_and_store_weather() em main.py.

O segundo gera `weather_dashboard.csv` com os registros do banco.

Para visualizar os dados atualizados, carregue o CSV no Tableau Public.

### Executar os testes

```powershell
.\.venv\Scripts\python.exe -m pytest -q
```

## Limitações atuais

A coleta e a exportação são executadas manualmente.
O painel utiliza o CSV carregado no Tableau, sem atualização automática.
Os horários das observações são armazenados em UTC.

## Próximas melhorias

- Automatizar a coleta com n8n.
- Adicionar gráficos de evolução com o crescimento do histórico.
