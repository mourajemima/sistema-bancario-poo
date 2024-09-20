from abc import ABC

class Cliente:
    def __init__(self, endereco):
        self.endereco = endereco
        self.contas = []

    def realizar_transacao(self, conta, transacao):
        transacao.registrar(conta)

    def adicionar_conta(self, conta):
        self.contas.append(conta)


class PessoaFisica(Cliente):
    def __init__(self, nome, data_nascimento, cpf, endereco):
        super().__init__(endereco)
        self.nome = nome
        self.data_nascimento = data_nascimento
        self.cpf = cpf


class Conta:
    def __init__(self, numero, cliente):
        self._saldo = 0
        self._numero = numero
        self._agencia = '0001'
        self._cliente = cliente
        self._historico = Historico()

    @classmethod
    def nova_conta(cls, cliente, numero):
        return cls(numero, cliente)
    
    @property
    def saldo(self):
        return self._saldo
    
    @property
    def numero(self):
        return self._numero

    @property
    def agencia(self):
        return self._agencia
    
    @property
    def cliente(self):
        return self._cliente
    
    @property
    def historico(self):
        return self._historico
    
    def sacar(self, valor):
        saldo = self.saldo
        
        if valor > saldo:
            print('Você não possui saldo suficinete.')
        elif valor > 0:
            self._saldo -= valor
            print('Saque realizado!')
            return True
        else:
            print('Não foi possível concluir a operação. Valor inserido é inválido.')

        return False
    
    def depositar(self, valor):
        if valor > 0:
            self._saldo += valor
            print('Deposito realizado!')
        else:
            print('Não foi possível concluir a operação. Valor inserido é inválido.')

        return True
    

class ContaCorrente(Conta):
    def __init__(self, numero, cliente, limite = 500, limite_saques = 3):
        super().__init__(numero, cliente)
        self.limite = limite
        self.limite_saques = limite_saques

    def sacar(self, valor):
        numero_saques = len([transacao for transacao in self.historico.transacoes if transacao['tipo'] == 'Saque'])

        if valor > self.limite:
            print('Valor superior ao limite do saque.')
        elif numero_saques >= self.limite_saques:
            print('Quantidade de saques excedida!')
        else:
            return super().sacar(valor)
        
        return False
    
    def __str__(self):
        return f'''
            Agência: {self.agencia}
            Conta Corrente: {self.numero}
            Titular: {self.cliente.nome}
        '''
    
class Historico:
    def transacoes(self):
        return self._transacoes
    
    def adicionar_transacao(self, transacao):
        self.transacoes.append(
            {
                'tipo': transacao.__class__.__name__,
                'valor': transacao.valor 
            }
        )

class Transacao(ABC):
    @property
    @abstractproperty
    def valor(self):
        pass

    @abstractclassmethod
    def registrar(self, contar):
        pass

class Saque(Transacao):
    def __init__(self, valor):
        self._valor = valor

    @property
    def valor(self):
        return self._valor
    
    def registrar(self, conta):
        if conta.sacar(self.valor):
            conta.historico.adicionar_transacao(self)

class Deposito(Transacao):
    def __init__(self, valor):
        self._valor = valor

    @property
    def valor(self):
        return self._valor
        
    def registrar(self, conta):
        if conta.depositar(self.valor):
            conta.historico.adicionar_transacao(self)