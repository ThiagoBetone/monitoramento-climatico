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

## Limitações atuais

A coleta e a exportação são executadas manualmente.
O painel utiliza o CSV carregado no Tableau, sem atualização automática.
Os horários das observações são armazenados em UTC.

## Próximas melhorias

- Documentar a instalação e execução.
- Automatizar a coleta com n8n.
- Adicionar gráficos de evolução com o crescimento do histórico.
