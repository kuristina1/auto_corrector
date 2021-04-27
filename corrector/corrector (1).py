import nltk
from collections import Counter
import re
from tkinter import *

with open("bidata.txt", encoding="utf-8") as f:
    big = f.read()
    pattern = "\.|\,|\?|\!|\-|\–|\«|\»"
    big2 = re.sub(pattern, "", big)


    # токенизируем
    tokens = nltk.word_tokenize(big2)


    word_counter = Counter(tokens)

    total_words = float(sum(word_counter.values()))

    # вероятность появления слова в корпусе - {слово: вероятность}
    word_probas = {word: word_counter[word] / total_words for word in word_counter.keys()}



    def dist0(word):
        return {word}

    def dist1(word):

        # Разбиваем слово на всевозможные части (левая - правая)
        pairs = [(word[:i], word[i:]) for i in range(len(word) + 1)]

        # переставляем последнюю букву левой части с первой буквой правой части
        transposition = []
        for a, b in pairs:
            if len(a) == 1:
                transposition.append(b[0] + a[0] + b[1:])
            if len(a) > 1 and len(b) != 0:
                transposition.append(a[0:-1] + b[0] + a[-1] + b[1:])

        # левая часть + правая часть без 1 буквы
        deletion = []
        for a, b in pairs:
            if len(b) != 0:
                deletion.append(a + b[1:])

        # заменяем первую букву правой части на каждую букву алфавита
        replacement = []
        alphabet = "абвгдеёжзийклмнопрстуфхцчшщъыьэюя"
        for a, b in pairs:
            for i in alphabet:
                if len(b) != 0:
                    replacement.append(a + i + b[1:])

        # вставляем букву из алфавита между левой и правой частью
        insertion = []
        for a, b in pairs:
            for i in alphabet:
                insertion.append(a + i + b)

        return set(transposition + deletion + replacement + insertion)

    # дублируем функцию на расстояние=1
    def dist2(word):
        return set(b for a in dist1(word) for b in dist1(a))

    def corrector(word):
        if word in tokens:
            return word

        suggestions = dist1(word) or dist2(word) or [word]
        d = {}
        best_candidate = []
        for w in suggestions:
            if w in tokens:
                best_candidate.append(w)

        for i in best_candidate:
            d[i] = word_probas[i]

        candidates = []
        for k in d.keys():
            candidates.append(k)

        return d

        # Еще один вариант исхода функции - return "Возможно вы имели в виду: " + str(candidates)



    def token(text):
        return re.findall(r'[а-я]+', text.lower())


    def correct_repeat(text):
        for i in token(text):
            if i not in tokens:
                for g in i:
                    pat = "{10}"
                    pat2 = g + pat
                    text = re.sub(pat2, g, text)

        return text


    user_text = input("""Введите, пожалуйста, текст, а затем нажмите "Enter": """)

    need_to_correct = token(user_text)

    correction_dictionary = {}
    for i in need_to_correct:
        correction_dictionary[i] = [corrector(i)]

    for k, v in correction_dictionary.items():
        v.append(correct_repeat(k))
        for i in v:
            if type(i) == dict:
                if len(i) == 0:
                    v.remove(i)
        if len(v) > 1:
            v.remove(v[1])

    for k, v in correction_dictionary.items():
        if k not in tokens:
            print("Ошибка в правописании:", k, "- Возможно вы имели в виду:", v)



















