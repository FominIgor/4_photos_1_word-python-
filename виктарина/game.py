import tkinter as tk
from PIL import Image, ImageTk
import random

class QuizGame:
    def __init__(self, root, database):
        self.root = root
        self.database = database 
        self.score = 0
        self.current_question_index = 0
        self.questions = list(self.database.keys())
        self.shuffle_questions()
        self.answer_length = 0  # Переменная для хранения количества букв в ответе
        self.attempts = 0  # Счетчик попыток

        self.root.configure(bg='#363636')  # Цвет фона для корневого окна

        self.question_label = tk.Label(root, text="Угадайте слово по фотографии:", bg='#363636', fg='#FF007F')
        self.question_label.pack()

        self.image_label = tk.Label(root)
        self.image_label.pack()

        self.answer_label = tk.Label(root, text="Ответ:", bg='#363636', fg='#FF007F')
        self.answer_label.pack()

        self.answer_entry = tk.Entry(root, highlightbackground='#FF007F')
        self.answer_entry.pack()

        self.submit_button = tk.Button(root, text="Ответить", command=self.check_answer, bg='#363636', fg='#FF007F', highlightbackground='#FF007F')
        self.submit_button.pack()

        self.result_label = tk.Label(root, text="", bg='#363636', fg='#FF007F')
        self.result_label.pack()

        self.hint_label = tk.Label(root, text="", bg='#363636', fg='#FF007F')
        self.hint_label.pack()

        self.update_question()

    def shuffle_questions(self):
        random.shuffle(self.questions)

    def update_question(self):
        if self.current_question_index < len(self.questions):
            question = self.questions[self.current_question_index]
            image_path = self.database[question]
            self.load_image(image_path)
            self.answer_length = len(question)  # Обновление количества букв в ответе
            self.attempts = 0  # Сброс счетчика попыток
        else:
            self.show_final_score()

    def load_image(self, image_path):
        image = Image.open(image_path)
        image = image.resize((300, 300))
        photo = ImageTk.PhotoImage(image)
        self.image_label.config(image=photo)
        self.image_label.photo = photo

    def check_answer(self):
        user_answer = self.answer_entry.get()
        correct_answer = self.questions[self.current_question_index]

        if user_answer == correct_answer:
            self.score += 1
            self.result_label.config(text="Правильно!")
            self.current_question_index += 1  # Переход к следующему вопросу
            self.answer_entry.delete(0, tk.END)
            self.hint_label.config(text="")  # Очистка текста подсказки
            self.update_question()
        else:
            self.attempts += 1
            if self.attempts == 2:  # Если счетчик попыток равен 2, показать правильный ответ
                self.result_label.config(text="Правильный ответ: " + correct_answer)
                self.attempts = 0  # Сбросить счетчик попыток
                self.hint_label.config(text="")  # Очистка текста подсказки
            else:
                self.result_label.config(text="Неверно.")
                self.hint_label.config(text=f"Подсказка: Ответ состоит из {self.answer_length} букв.")

    def show_final_score(self):
        self.question_label.config(text=f"Игра окончена. Ваш счет: {self.score}")

if __name__ == "__main__":
    root = tk.Tk()
    root.title("Игра викторина")

    database_file = "answers.txt"  # Укажите путь к вашему файлу базы данных
    database = {}

    with open(database_file, 'r', encoding='utf-8') as file:
        for line in file:
            image_path, word = line.strip().split(' |')
            database[word] = image_path

    game = QuizGame(root, database)
    root.mainloop()
