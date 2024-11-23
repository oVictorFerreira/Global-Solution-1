
# Calculadora de Consumo de Energia
João Victor da Silva Ferreira - RM 560439
Erick Cardoso - RM 560440
Davi Daparé - RM 560721

O programa ajuda a monitorar o consumo de energia de diferentes fontes (solar, eólica, hídrica e rede) e calcular com precisão os custos totais e as economias geradas pelo uso de energia renovável. Auxilia no planejamento financeiro, mostra quanto deve ser pago à concessionária e incentiva a redução do uso de energia não renovável. O programa aumenta a sensibilização para a sustentabilidade e destaca os benefícios ambientais e económicos de escolhas mais inteligentes. Ferramenta educacional prática para otimizar o consumo de energia.

## Funcionalidades

- Entrada de consumo para 4 fontes de energia:
  - Solar
  - Eólica
  - Hidrelétrica
  - Rede Elétrica
- Cálculo de:
  - Energia renovável total utilizada
  - Energia não renovável utilizada
  - Consumo total
  - Economia gerada pelo uso de energia renovável
  - Valor devido à concessionária com base em uma tarifa fixa e variável
- Opção de detalhar o consumo de uma fonte específica escolhida pelo usuário.

## Como Usar

1. Certifique-se de ter o Python 3 instalado.
2. Copie o código do arquivo `GS.py` para o seu ambiente.
3. Execute o programa
4. Insira os valores de consumo para cada fonte de energia quando solicitado.
5. Consulte os cálculos exibidos, incluindo total de consumo, economia gerada e valor devido.

## Exemplo de Uso

Entrada:
```
Digite o consumo de energia Solar (em watts): 500
Digite o consumo de energia Eólica (em watts): 300
Digite o consumo de energia Hidrelétrica (em watts): 200
Digite o consumo de energia Rede Elétrica (em watts): 100
Escolha uma fonte de energia para mais detalhes (0-Sair, 1-Solar, 2-Eólica, 3-Hidrelétrica, 4-Rede Elétrica): 1
```

Saída:
```
Detalhamento do Consumo de Energia:
 - Solar: 500.00 watts
 - Eólica: 300.00 watts
 - Hidrelétrica: 200.00 watts
 - Rede Elétrica: 100.00 watts

Total de Energia Renovável: 1000.00 watts
Total de Energia Não Renovável: 100.00 watts
Consumo Total: 1100.00 watts
Economia com energia renovável: R$656.00
Valor devido à concessionária: R$130.56 (Tarifa fixa: R$65.00, Variável: R$65.56)

Você escolheu Solar com consumo de 500.00 watts.
```

## Configurações

- **Tarifa fixa**: R$65,00
- **Tarifa variável por kWh**: R$0,656

Esses valores podem ser ajustados diretamente no código, nas variáveis `tarifafixa` e `custokwh`.

## Requisitos

- Python 3.6 ou superior.

## Personalização

- Para adicionar novas fontes de energia, inclua-as na lista `fontes` e ajuste os cálculos no código.
- Alterar tarifas fixas e variáveis para refletir os custos locais.

Se tiver dúvidas ou sugestões, entre em contato! 
