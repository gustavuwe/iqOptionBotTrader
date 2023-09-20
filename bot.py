from dataclasses import dataclass, asdict
from pathlib import Path
from tinydb import TinyDB
from iqoptionapi.stable_api import IQ_Option
import time

email = 'gustavuwe.123@gmail.com'
senha = 'ggpranois123'

API = IQ_Option(email,senha)

### Função para conectar na IQOPTION ###
check, reason = API.connect()
if check:
    print('Conectado com sucesso')
else:
    if reason == '{"code":"invalid_credentials","message":"You entered the wrong credentials. Please ensure that your login/password is correct."}':
        print('Email ou senha incorreta')
        
    else:
        print('Houve um problema na conexão')

        print(reason)

### Função para Selecionar demo ou real ###
while True:
    escolha = input('Selecione a conta em que deseja conectar: demo ou real  - ')
    if escolha == 'demo':
        conta = 'PRACTICE'
        print('Conta demo selecionada')
        break
    if escolha == 'real':
        conta = 'REAL'
        print('Conta real selecionada')
        break
    else:
        print('Escolha incorreta! Digite demo ou real')
        
API.change_balance(conta)

### Função abrir ordem e checar resultado ###
def compra(ativo,valor,direcao,exp,tipo):
    if tipo == 'digital':
        check, id = API.buy_digital_spot_v2(ativo,valor,direcao,exp)
    else:
        check, id = API.buy(valor,ativo,direcao,exp)


    if check:
        print('Ordem executada ',id)

        while True:
            time.sleep(0.1)
            status , resultado = API.check_win_digital_v2(id) if tipo == 'digital' else API.check_win_v4(id)
            result = ""

            if status:
                if resultado > 0:
                    print('WIN', round(resultado,2))
                    result = "WIN"
                elif resultado == 0:
                    print('EMPATE', round(resultado,2))
                    result = "EMPATE"
                else:
                    print('LOSS', round(resultado,2))
                    result = "LOSS"

                @dataclass
                class Logs:
                    conta: str
                    valor: int
                    ativo: str
                    tipo: str
                    result: str

                    def as_dict(self):
                        return asdict(self)

                t1 = Logs(conta, valor, ativo, tipo, result)

                db_path = Path(__file__).parent / 'db.json'
                db = TinyDB(db_path, indent=4)

                db.insert(t1.as_dict())

                break

    else:
        print('erro na abertura da ordem,', id)
        

#ativo = 'EURUSD'
#valor = 10.50
#direcao = 'call'
#exp = 1
#tipo = 'digital'

ativo = input('\n >> Digite o ativo que você deseja operar: ').upper()
valor = input('\n >> Digite o valor de entrada: ')
direcao = input('\n >> Entrada para call ou put? ')
exp = input('\n >> Qual timeframe? ')
tipo = input('\n >> digital ou binarias? ')

### chamada da função de compra ###
compra(ativo,valor,direcao,exp,tipo)