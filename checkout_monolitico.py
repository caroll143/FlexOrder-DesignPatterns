from __future__ import annotations
from abc import ABC, abstractmethod
from dataclasses import dataclass, field
from typing import List

# --- Modelos simples ---
@dataclass
class Item:
    nome: str
    valor: float


@dataclass
class Pedido:
    itens: List[Item]
    pagamento: "EstrategiaPagamento"
    frete: "EstrategiaFrete"
    tem_embalagem_presente: bool = False
    valor_base: float = field(init=False)

    def __post_init__(self):
        self.valor_base = sum(i.valor for i in self.itens)

    def set_pagamento(self, pagamento: "EstrategiaPagamento"):
        self.pagamento = pagamento

    def set_frete(self, frete: "EstrategiaFrete"):
        self.frete = frete


# --- Estratégias de Pagamento ---
class EstrategiaPagamento(ABC):
    @abstractmethod
    def processar_pagamento(self, valor: float) -> bool:
        pass


class PagamentoPix(EstrategiaPagamento):
    def processar_pagamento(self, valor: float) -> bool:
        print(f"Processando R${valor:.2f} via PIX...")
        print("   -> Pagamento com PIX APROVADO (QR Code gerado).")
        return True


class PagamentoCredito(EstrategiaPagamento):
    def processar_pagamento(self, valor: float) -> bool:
        print(f"Processando R${valor:.2f} via Cartão de Crédito...")
        if valor < 1000:
            print("   -> Pagamento com Credito APROVADO.")
            return True
        print("   -> Pagamento com Credito REJEITADO (limite excedido).")
        return False


class PagamentoTransferencia(EstrategiaPagamento):
    def processar_pagamento(self, valor: float) -> bool:
        print(f"Processando R${valor:.2f} via Transferência...")
        print("   -> Pagamento via transferencia APROVADO (pode demorar).")
        return True


# --- Estratégias de Frete ---
class EstrategiaFrete(ABC):
    @abstractmethod
    def calcular(self, valor_com_desconto: float) -> float:
        pass


class FreteNormal(EstrategiaFrete):
    def calcular(self, valor_com_desconto: float) -> float:
        custo = valor_com_desconto * 0.05
        print(f"Frete Normal: R${custo:.2f}")
        return custo


class FreteExpresso(EstrategiaFrete):
    def calcular(self, valor_com_desconto: float) -> float:
        custo = valor_com_desconto * 0.10 + 15.00
        print(f"Frete Expresso (com taxa): R${custo:.2f}")
        return custo


class FreteTeletransporte(EstrategiaFrete):
    def calcular(self, valor_com_desconto: float) -> float:
        custo = 50.00
        print(f"Frete Teletransporte: R${custo:.2f}")
        return custo


# --- Calculadora (regras de desconto/taxa) ---
class CalculadoraPedido:
    EMBALAGEM_TAXA = 5.0

    def __init__(self, pedido: Pedido):
        self.pedido = pedido

    def valor_apos_descontos(self) -> float:
        base = self.pedido.valor_base
        # prioridade: PIX primeiro
        if isinstance(self.pedido.pagamento, PagamentoPix):
            print("Aplicando 5% de desconto PIX.")
            return base * 0.95
        # se não for PIX, verificar pedido grande
        if base > 500:
            print("Aplicando 10% de desconto para pedidos grandes.")
            return base * 0.90
        return base

    def valor_com_embalagem(self, valor_sem_embalagem: float) -> float:
        if self.pedido.tem_embalagem_presente:
            print(f"Adicionando R${self.EMBALAGEM_TAXA:.2f} de Embalagem de Presente.")
            return valor_sem_embalagem + self.EMBALAGEM_TAXA
        return valor_sem_embalagem

    def calcular_totais(self) -> tuple[float, float, float]:
        valor_descontado = self.valor_apos_descontos()
        frete = self.pedido.frete.calcular(valor_descontado)
        valor_com_emb = self.valor_com_embalagem(valor_descontado)
        valor_final = valor_com_emb + frete
        return valor_descontado, frete, valor_final


# --- Subsistemas ---
class SistemaEstoque:
    def registrar_pedido(self, pedido: Pedido):
        print("SistemaEstoque: Registrando itens no estoque.")


class GeradorNotaFiscal:
    def gerar(self, pedido: Pedido, valor: float):
        print(f"GeradorNotaFiscal: Nota fiscal gerada para valor R${valor:.2f}.")


# --- Facade / Orquestrador de checkout ---
class Checkout:
    def __init__(self):
        self.estoque = SistemaEstoque()
        self.gerador_nf = GeradorNotaFiscal()

    def concluir(self, pedido: Pedido) -> bool:
        print("=========================================")
        print("Iniciando processo de checkout...")
        print("=========================================")

        calc = CalculadoraPedido(pedido)
        valor_descontado, frete, valor_final = calc.calcular_totais()

        print(f"\nValor a Pagar: R${valor_final:.2f}")

        if pedido.pagamento.processar_pagamento(valor_final):
            self.estoque.registrar_pedido(pedido)
            self.gerador_nf.gerar(pedido, valor_final)
            print("\nSUCESSO: Pedido finalizado e registrado no estoque.")
            return True

        print("\nFALHA: Transação abortada.")
        return False


# --- Exemplo de uso ---
if __name__ == "__main__":
    itens_p1 = [
        Item("Capa da Invisibilidade", 150.0),
        Item("Poção de Voo", 80.0),
    ]
    pedido1 = Pedido(
        itens=itens_p1,
        pagamento=PagamentoPix(),
        frete=FreteNormal(),
        tem_embalagem_presente=False,
    )
    Checkout().concluir(pedido1)

    print("\n--- Próximo Pedido ---\n")

    itens_p2 = [Item("Cristal Mágico", 600.0)]
    pedido2 = Pedido(
        itens=itens_p2,
        pagamento=PagamentoCredito(),
        frete=FreteExpresso(),
        tem_embalagem_presente=True,
    )
    Checkout().concluir(pedido2)

    print("\n--- Exemplo de troca de estratégia em tempo de execução ---\n")
    pedido2.set_frete(FreteTeletransporte())
    pedido2.set_pagamento(PagamentoTransferencia())
    Checkout().concluir(pedido2)