from typing import List, Optional
from abc import ABC, abstractmethod
import random

class Tabuleiro:
    """
    Classe que representa o tabuleiro do jogo da velha.
    """
    def __init__(self):
        """
        Inicializa o tabuleiro vazio.
        """
        self.casas = [' ' for _ in range(9)]

    def pegar_tabuleiro(self) -> List[List[str]]:
        """
        Retorna o tabuleiro no formato de lista de listas.

        Returns:
        --------
        List[List[str]]:
            O tabuleiro dividido em linhas.
        """
        return [self.casas[i:i + 3] for i in range(0, 9, 3)]

    def marcar_casa(self, pos: tuple[int, int], valor: str):
        """
        Marca uma casa com o símbolo do jogador.

        Parâmetros:
        -----------
        pos : tuple[int, int]
            A posição (linha, coluna) da jogada.
        valor : str
            O símbolo do jogador ('X' ou 'O').

        Raises:
        -------
        ValueError:
            Se a casa já estiver marcada.
        """
        index = pos[0] * 3 + pos[1]
        if self.casas[index] == ' ':
            self.casas[index] = valor
        else:
            raise ValueError("Casa já marcada!")

    def imprimir_tabuleiro(self):
        """
        Imprime o tabuleiro na tela com separadores.
        """
        tabuleiro = self.pegar_tabuleiro()
        for linha in tabuleiro:
            print('|'.join(linha))
            print('-' * 5)

class Jogador(ABC):
    """
    Classe abstrata para representar um jogador.
    """
    def __init__(self, nome: str, simbolo: str):
        """
        Inicializa o jogador com nome e símbolo.

        Parâmetros:
        -----------
        nome : str
            O nome do jogador.
        simbolo : str
            O símbolo do jogador ('X' ou 'O').
        """
        self.nome = nome
        self.simbolo = simbolo

    @abstractmethod
    def fazer_jogada(self, tabuleiro: 'Tabuleiro') -> tuple[int, int]:
        """
        Método abstrato para realizar uma jogada.

        Parâmetros:
        -----------
        tabuleiro : Tabuleiro
            O tabuleiro do jogo.

        Returns:
        --------
        tuple[int, int]:
            A posição da jogada (linha, coluna).
        """
        pass

class JogadorHumano(Jogador):
    """
    Classe que representa um jogador humano.
    """
    def fazer_jogada(self, tabuleiro: 'Tabuleiro') -> tuple[int, int]:
        """
        Solicita uma jogada ao jogador humano.

        Returns:
        --------
        tuple[int, int]:
            A posição escolhida pelo jogador (linha, coluna).
        """
        while True:
            try:
                pos = input(f"Jogador {self.simbolo}, insira sua jogada (linha,coluna): ")
                linha, coluna = map(int, pos.split(','))
                return linha, coluna
            except ValueError:
                print("Entrada inválida, tente novamente.")

class JogadorComputador(Jogador):
    """
    Classe que representa um jogador computador.
    """
    def __init__(self, nome: str, simbolo: str, estrategia: str):
        """
        Inicializa o jogador computador com uma estratégia.

        Parâmetros:
        -----------
        nome : str
            O nome do jogador.
        simbolo : str
            O símbolo do jogador ('X' ou 'O').
        estrategia : str
            A estratégia do computador (atualmente 'aleatoria').
        """
        super().__init__(nome, simbolo)
        self.estrategia = estrategia
        if estrategia not in ['aleatoria']:
            raise ValueError("Estratégia inválida!")

    def fazer_jogada(self, tabuleiro: 'Tabuleiro') -> tuple[int, int]:
        """
        Determina a jogada com base na estratégia.

        Returns:
        --------
        tuple[int, int]:
            A posição escolhida (linha, coluna).
        """
        if self.estrategia == 'aleatoria':
            casas_vazias = [i for i, casa in enumerate(tabuleiro.casas) if casa == ' ']
            if casas_vazias:
                jogada = random.choice(casas_vazias)
                return divmod(jogada, 3)

class JogoVelha:
    """
    Classe que representa a mecânica do jogo da velha.
    """
    def __init__(self, jogador1: Jogador, jogador2: Jogador):
        """
        Inicializa o jogo da velha com dois jogadores e um tabuleiro vazio.

        Parâmetros:
        -----------
        jogador1 : Jogador
            O primeiro jogador (pode ser humano ou computador).
        jogador2 : Jogador
            O segundo jogador (pode ser humano ou computador).
        """
        self.jogadores = [jogador1, jogador2]
        self.tabuleiro = Tabuleiro()
        self.turno = 0

    def jogador_atual(self) -> Jogador:
        """
        Retorna o jogador atual com base no turno.

        Returns:
        --------
        Jogador:
            O jogador que deve realizar a próxima jogada.
        """
        return self.jogadores[self.turno % 2]

    def checar_fim_de_jogo(self) -> Optional[str]:
        """
        Verifica se o jogo terminou e retorna a condição de vitória ou empate.

        Returns:
        --------
        Optional[str]:
            String de vitória/empate ou None se o jogo ainda não acabou.
        """
        # Verifica as linhas
        for i in range(0, 9, 3):
            if self.tabuleiro.casas[i] == self.tabuleiro.casas[i+1] == self.tabuleiro.casas[i+2] != ' ':
                return f"Jogador {self.tabuleiro.casas[i]} venceu completando uma linha!"

        # Verifica as colunas
        for i in range(3):
            if self.tabuleiro.casas[i] == self.tabuleiro.casas[i+3] == self.tabuleiro.casas[i+6] != ' ':
                return f"Jogador {self.tabuleiro.casas[i]} venceu completando uma coluna!"

        # Verifica as diagonais
        if self.tabuleiro.casas[0] == self.tabuleiro.casas[4] == self.tabuleiro.casas[8] != ' ':
            return f"Jogador {self.tabuleiro.casas[0]} venceu completando uma diagonal!"
        if self.tabuleiro.casas[2] == self.tabuleiro.casas[4] == self.tabuleiro.casas[6] != ' ':
            return f"Jogador {self.tabuleiro.casas[2]} venceu completando uma diagonal!"

        # Verifica se o tabuleiro está completo (empate)
        if ' ' not in self.tabuleiro.casas:
            return "Empate! Todas as casas foram preenchidas."

        return None  # O jogo ainda não acabou

    def jogar(self):
        """
        Executa o loop principal do jogo, alternando entre os jogadores e verificando o fim do jogo.
        """
        while True:
            jogador = self.jogador_atual()
            print(f"Turno do jogador: {jogador.simbolo}")
            pos = jogador.fazer_jogada(self.tabuleiro)
            self.tabuleiro.marcar_casa(pos, jogador.simbolo)
            self.tabuleiro.imprimir_tabuleiro()

            fim_de_jogo = self.checar_fim_de_jogo()
            if fim_de_jogo:
                print(fim_de_jogo)
                break

            self.turno += 1