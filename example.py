from jogovelha import JogoVelha, JogadorHumano, JogadorComputador

def main():
    """
    Função principal que inicializa e executa o jogo.
    """
    jogador1 = JogadorHumano("Jogador 1", "X")
    jogador2 = JogadorComputador("Computador", "O", "aleatoria")

    jogo = JogoVelha(jogador1, jogador2)
    jogo.jogar()

if __name__ == "__main__":
    main()