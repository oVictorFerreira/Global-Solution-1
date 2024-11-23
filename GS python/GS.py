def calcularrenovavel(solar, eolica, hidreletrica):
    return solar + eolica + hidreletrica

def calculartotal(renovavel, naorenovavel):
    return renovavel + naorenovavel

def calculareconomia(renovavel, custokwh): #Valor que seria pago se fosse energia da rede eletrica
    return renovavel * custokwh

def calculardevido(naorenovavel, custokwh, tarifafixa):
    gastorede = naorenovavel * custokwh
    return tarifafixa + gastorede, gastorede

def main():
    # Tarifas
    custokwh = 0.656  
    tarifafixa = 65.00

    # Listas das energias
    fontes = ["Solar", "Eólica", "Hidrelétrica", "Rede Elétrica"]
    energias = []
    for fonte in fontes: #fonte = index e fontes = lista
        consumo = float(input(f"Digite o consumo de energia {fonte} (em kWh): ")) #Pega a quantidade de watts utilizada de cada fonte. 
        energias.append(consumo) #Add consumo a lista de energias

    # Chama os funções que fazem os calculos
    renovavel = calcularrenovavel(energias[0], energias[1], energias[2])  # Solar, Eólica, Hidrelétrica
    naorenovavel = energias[3] #Rede elétrica
    total = calculartotal(renovavel, naorenovavel) 
    economia = calculareconomia(renovavel, custokwh)
    valordevido, gastorede = calculardevido(naorenovavel, custokwh, tarifafixa)

    # Resultados
    print("\nDetalhamento do Consumo de Energia:")
    for i in range(len(fontes)):
        print(f" - {fontes[i]}: {energias[i]:.2f} kWh")
    print(f"\nTotal de Energia Renovável: {renovavel:.2f} kWh")
    print(f"Total de Energia Não Renovável: {naorenovavel:.2f} kWh")
    print(f"Consumo Total: {total:.2f} kWh")
    print(f"Economia com energia renovável: R${economia:.2f}")
    print(f"Valor devido à concessionária: R${valordevido:.2f} (Tarifa fixa: R${tarifafixa:.2f}, Variável: R${gastorede:.2f})")

    # Seleção de fonte de energia
    while True:
        escolha = int(input("\nEscolha uma fonte de energia para mais detalhes (0-Sair, 1-Solar, 2-Eólica, 3-Hidrelétrica, 4-Rede Elétrica): "))
        if 1 <= escolha <= 4:
            print(f"\nVocê escolheu: {fontes[escolha - 1]}, seu consumo foi de {energias[escolha - 1]:.2f} kWh.")
        elif escolha == 0:
            print(f"\nTenha um ótimo dia!")
            break
        else:
            print("\nOpção inválida.")

# Chama a função main (principal)
main()
