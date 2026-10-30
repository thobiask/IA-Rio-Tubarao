# Experimento V73 — classificação de elevações diárias

Este diretório contém o **script original** `experimento_v73.py`, preservado sem alterações.

## Entrada

O script procura a base em:

```python
SOURCE=Path('/mnt/data/base_tratada_ia_com_metadados.csv')
```

Para executar fora do ambiente original, é necessário adaptar esse caminho à localização da base validada. A alteração ainda **não foi incorporada ao código histórico**, para preservar a rastreabilidade.

## Ambiente

Dependências principais: `numpy`, `pandas` e `scikit-learn`. As versões exatas usadas originalmente não foram registradas neste arquivo e ainda precisam ser determinadas; portanto, `requirements.txt` não constitui um lockfile reprodutível.

## Método

- Alvo: nível no dia seguinte na estação 84580000 (Rio do Pouso).
- Preditores: níveis e variações do alvo e níveis disponíveis de quatro estações auxiliares.
- Separação temporal: treino até 2015, validação 2016–2020, teste 2021–2025.
- Limiares de elevação: 50 e 100 cm.
- Modelos: regressão logística e HistGradientBoosting.
- Seleção de limiar de decisão somente na validação.

## Limitações

Os dados são diários; não está confirmada a disponibilidade operacional de cada observação na hora da emissão. As elevações não representam necessariamente enchentes. Os resultados publicados são retrospectivos e não habilitam alertas reais.

## Estado de publicação

- [x] Script original publicado e hash Git comparado com o pacote local.
- [x] CSV de métricas e limiares publicado e hashes conferidos.
- [ ] Base de entrada publicada e licença auditada.
- [ ] Reexecução independente validada.
