import random
import re
from constants import DIFFICULTY_LEVELS, WORDS_LENGTHS


def show_difficulty_menu():
    """Exibe o menu que permite o jogador selecionar o nivel de dificuldade
        :return: Uma string representando nível de dificuldade
    """
    difficulty_setting = ""

    print("Escolha um nível de dificuldade:")

    while not difficulty_setting:
        for k, v in DIFFICULTY_LEVELS.items():
            print(f"{k} - {v}")

        difficulty_setting = input("Escolha um número ")

        if difficulty_setting not in DIFFICULTY_LEVELS.keys():
            print(f"{difficulty_setting} não é uma opção válida.")
            difficulty_setting = ""  # manter no loop até que selecione uma chave key válida

    return difficulty_setting


def get_random_word(difficulty_setting):
    """
    Abre o arquivo que contém o banco de palavras e seleciona uma palavra aleatoriamente,
    baseado no parametro difficulty setting.
    :param difficulty_setting: string que representa o nível de dificuldade selecionado
    pelo usuário
    :return:string que representa a palavra aleatoriamente selecionada.
    """

    with open("static/words.txt", mode="r") as f_words:
        words = []
        for word in f_words.readlines():
            w = word.strip()
            min, max = WORDS_LENGTHS[difficulty_setting]

            if min <= len(w) <= max:
                words.append(w)  # a lista de palavras possíveis é recriada apenas com as palavras de qtd selecionada.

        max_index = len(words) - 1
        generate_random_index = random.randint(0, max_index)
        selected_word = words[generate_random_index]

        return selected_word


def get_total_tries(selected_word, difficulty_setting):
    """
    Obtém a quantidade de chances que o jogador têm para adivinhar a palavra.
    :param selected_word: string que possui a palavra selecionada aleatóriamente.
    :param difficulty_setting: string que representa o nível de dificuldade escolhida.
    :return: None
    """
    unique_letters = set(selected_word)
    total_tries = 1.5 * len(unique_letters)
    if difficulty_setting == "1":
        total_tries += 2
    elif difficulty_setting == "3":
        total_tries -= 2
        total_tries = min([total_tries, 18])

    total_tries = round(total_tries)
    return total_tries


def play_hangman(selected_word, difficulty_setting):
    """
    Simula o jogo da forca.
    :param selected_word: string/palavra a ser adivinhada
    :param difficulty_setting: string que representa a dificuldade escolhida.
    :return: int que, caso positivo, significa que o jogador ganhou.
    """
    total_tries = available_tries = get_total_tries(selected_word=selected_word, difficulty_setting=difficulty_setting)
    current_state = ["_" for letter in selected_word]
    guessed_letters = []

    while "_" in current_state and available_tries:
        print(f"\n\n### Tentativa número {total_tries - available_tries + 1} de {total_tries} ###")
        for char in current_state:
            print(char, end=" ")

        guess = ""
        while not guess:
            guess = input("\nTente uma letra: ").lower()
            if len(guess) != 1 or not re.match("[a-z]", guess):
                print("Entrada inválida. Tente novamente, entrando apenas 1 letra.")
                guess = ""

        if guess not in guessed_letters:
            guessed_letters.append(guess)

            if guess in selected_word:
                positions = [m.start() for m in re.finditer(guess, selected_word)]

                for index in positions:
                    current_state[index] = guess

            else:
                available_tries -= 1
        else:
            print(f"{guess} já foi tentado anteriormente.")

    return available_tries
