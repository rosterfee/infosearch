from tkinter import *
from tkinter import ttk
from search import get_search_results


# Создаем окно приложения
window = Tk()
window.geometry('500x500')
window.title("Поиск")


# Создаем функцию для поиска
def search():
    # Отчищаем список результатов от предыдущего поиска
    results.delete(0, END)

    # Получаем текст из строки поиска
    query = search_box.get()
    result_links = get_search_results(query)

    counter = 1
    for link in result_links.values():
        results.insert(END, f'{counter}. {link}')
        counter += 1


# Создаем строку поиска
search_box = ttk.Entry(window, width=200)
search_box.pack()

# Создаем кнопку для поиска
search_button = ttk.Button(window, text="Поиск", command=search, width=200)
search_button.pack()

# Создаем список результатов поиска
results = Listbox(window, height=300, width=300)
results.pack()

# Запускаем приложение
window.mainloop()
