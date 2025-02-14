import datetime
import time
import os

now = datetime.datetime.now() #Import e formatação da data e hora
dateandtime = now.strftime("%d/%m/%Y %H:%M:%S")


TARIFA_ENERGIA = 0.58  # Tarifa média de energia em São Paulo em R$/kWh (Eletropaulo Metropolitana Eletricidade de São Paulo S/A)

dados = [
    {"valor_conta": 100, "consumo": 172, "potencia": 1.14, "investimento_min": 6813.17, "investimento_max": 9084.23, "economia_mensal": 71},
    {"valor_conta": 200, "consumo": 344, "potencia": 2.73, "investimento_min": 12307.37, "investimento_max": 17777.32, "economia_mensal": 171},
    {"valor_conta": 500, "consumo": 862, "potencia": 7.53, "investimento_min": 30132.47, "investimento_max": 43692.08, "economia_mensal": 471},
    {"valor_conta": 1000, "consumo": 1724, "potencia": 15.53, "investimento_min": 59014.21, "investimento_max": 88521.32, "economia_mensal": 971},
    {"valor_conta": 15000, "consumo": 25862, "potencia": 239.44, "investimento_min": 1436664.38, "investimento_max": 1915552.50, "economia_mensal": 14971}
]

# Função q calcula o consumo mensal em kWh com base no valor da conta
def calcular_consumo(valor_conta):
    return valor_conta / TARIFA_ENERGIA

# Onde é feita a interpolação dos dados
def interpolar(valor, chave):
    for i in range(1, len(dados)):
        if valor <= dados[i]["valor_conta"]:
            x1, y1 = dados[i-1]["valor_conta"], dados[i-1][chave]
            x2, y2 = dados[i]["valor_conta"], dados[i][chave]
            return y1 + (valor - x1) * (y2 - y1) / (x2 - x1)
    return dados[-1][chave]  

# Onde é calculado o custo estimado do sistema
def calcular_custo(valor_conta):
    investimento_min = interpolar(valor_conta, "investimento_min")
    investimento_max = interpolar(valor_conta, "investimento_max")
    return (investimento_min + investimento_max) / 2

# Aq é pra calcular a economia anual
def calcular_economia_anual(valor_conta):
    economia_mensal = interpolar(valor_conta, "economia_mensal")
    return economia_mensal * 12

# Aqui é calculado o tempo de retorno do investimento
def calcular_retorno_investimento(custo, economia_anual):
    if economia_anual == 0:
        return float('inf')
    return custo / economia_anual

# Função para mostrar o menu
def mostrar_menu():
    print("|                                           |")
    print("|   CALCULADORA SOLAR FOTOVOLTAICA          |")
    print("|                                           |")
    print("| 1. Calcular Potência do Sistema           |")
    print("| 2. Calcular Custo do Sistema              |")
    print("| 3. Estimar Economia Anual                 |")
    print("| 4. Simular Retorno sobre Investimento     |")
    print("| 5. Fechar o Menu                          |")
    print("|                                           |")
    print("| " + dateandtime + "                       |")
    print("|                                           |")

# Função principal do menu
def main():
    continua = True
    while continua:
        try:
            mostrar_menu()
            opcao = int(input("Escolha uma opção (1-5): "))

            if opcao in [1, 2, 3, 4]:
                # Solicita o valor da conta apenas após a escolha de uma opção válida
                valor_conta = float(input("Digite o valor da conta de energia (em R$): "))
                if valor_conta < 100 or valor_conta > 15000:
                    print("Valor inválido! O valor da conta deve ser entre R$ 100 e R$ 15.000.")
                    time.sleep(2)
                    continue
                
            if opcao == 1:
                potencia = interpolar(valor_conta, "potencia")
                print(f"\nPotência do Sistema Necessária: {potencia:.2f} kWp")
                print("\nLembrando, esses dados são estimativos e podem ter uma margem de variaração.")
                time.sleep(3)
            elif opcao == 2:
                custo = calcular_custo(valor_conta)
                print(f"\nCusto Estimado do Sistema: R$ {custo:.2f}")
                print("\nLembrando, esses dados são estimativos e podem ter uma margem de variaração.")
                time.sleep(3)
            elif opcao == 3:
                economia_anual = calcular_economia_anual(valor_conta)
                print(f"\nEconomia Anual Estimada: R$ {economia_anual:.2f}")
                print("\nLembrando, esses dados são estimativos e podem ter uma margem de variaração.")
                time.sleep(3)
            elif opcao == 4:
                custo = calcular_custo(valor_conta)
                economia_anual = calcular_economia_anual(valor_conta)
                retorno_investimento = calcular_retorno_investimento(custo, economia_anual)
                print(f"\nTempo médio para o retorno do Investimento: {retorno_investimento:.1f} anos")
                print("\nLembrando, esses dados são estimativos e podem ter uma margem de variaração.")
                time.sleep(3)
            elif opcao == 5:
                os.system('cls' if os.name == 'nt' else 'clear')
                print("Fechando o menu... \nAté mais!\n")
                continua = False
            else:
                print("Opção inválida! Escolha uma opção de 1 a 5.")
                time.sleep(1.5)
        except ValueError:
            print("Por favor, insira um valor válido.")
            time.sleep(1.5)

# Executando o menu
main()
