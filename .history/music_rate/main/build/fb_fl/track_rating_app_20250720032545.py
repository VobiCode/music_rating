import tkinter as tk
from tkinter import ttk
from datetime import datetime
import os
import subprocess
import re
import sys

def sanitize_filename(name):
    return re.sub(r'[^a-zA-Zа-яА-Я0-9_]', '_', name.strip().replace(' ', '_'))

def update_score():
    track = track_name.get().strip()
    if not track:
        score_var.set("Введите название трека!")
        return

    main_score = sum(slider.get() for slider in sliders[:4])
    bonus_score = sliders[4].get() + sliders[5].get()
    total_score = main_score + bonus_score

    score_var.set(
        f"{sliders[0].get()} + {sliders[1].get()} + {sliders[2].get()} + {sliders[3].get()} + {sliders[4].get()} + {sliders[5].get()} = {total_score} БАЛЛОВ"
    )

def calculate_score():
    track = track_name.get().strip()
    if not track:
        score_var.set("Введите название трека!")
        return

    if getattr(sys, 'frozen', False):
        exe_dir = os.path.dirname(sys.executable)
        main_dir = exe_dir
    else:
        current_dir = os.path.dirname(os.path.abspath(__file__))
        main_dir = os.path.join(current_dir, "main")
    
    obsidian_dir = None
    current_path = main_dir
    while current_path and current_path != os.path.dirname(current_path):
        obsidian_folder = os.path.join(current_path, ".obsidian")
        obsidian_file = os.path.join(current_path, ".obsidian.vault")
        if os.path.exists(obsidian_folder) or os.path.exists(obsidian_file):
            obsidian_dir = current_path
            break
        current_path = os.path.dirname(current_path)
    
    user_vault = vault_path.get().strip()
    if user_vault and os.path.exists(user_vault):
        rating_dir = os.path.join(user_vault, "rating_result")
    elif obsidian_dir:
        rating_dir = os.path.join(obsidian_dir, "rating_result")
    else:
        rating_dir = os.path.join(main_dir, "rating_result")
    
    if not os.path.exists(rating_dir):
        os.makedirs(rating_dir)

    safe_name = sanitize_filename(track)
    md_filename = f"{safe_name}_score.md"
    md_path = os.path.join(rating_dir, md_filename)

    main_score = sum(slider.get() for slider in sliders[:4])
    bonus_score = sliders[4].get() + sliders[5].get()
    total_score = main_score + bonus_score

    with open(md_path, "w", encoding="utf-8") as f:
        f.write(f"# {track}\n")
        f.write(f"_Оценка: {datetime.now().strftime('%Y-%m-%d %H:%M')}_\n\n")
        labels = [
            "Рифмы и/или Образы",
            "Структура и/или Ритмика",
            "Реализация выбранного стиля",
            "Индивидуальность и/или Харизма",
            "Атмосфера и/или Вайб",
            "Трендовость и/или Популярность"
        ]
        for i in range(6):
            f.write(f"- **{labels[i]}**: {sliders[i].get()}\n")
        f.write(f"\n**Общий балл:** {total_score}\n")


    open_folder(md_path)
    
    short_path = os.path.basename(md_path)
    score_var.set(f"Файл создан:\n{short_path}\nв папке:\n{os.path.dirname(md_path)}")

def open_folder(filepath):
    folder_path = os.path.dirname(filepath)
    if os.name == 'nt':
        subprocess.Popen(f'explorer "{folder_path}"')
    elif os.name == 'posix':
        subprocess.Popen(['open', folder_path])

def open_rating_folder():
    if getattr(sys, 'frozen', False):
        exe_dir = os.path.dirname(sys.executable)
        main_dir = exe_dir
    else:
        current_dir = os.path.dirname(os.path.abspath(__file__))
        main_dir = os.path.join(current_dir, "main")
    
    obsidian_dir = None
    current_path = main_dir
    while current_path and current_path != os.path.dirname(current_path):
        obsidian_folder = os.path.join(current_path, ".obsidian")
        obsidian_file = os.path.join(current_path, ".obsidian.vault")
        if os.path.exists(obsidian_folder) or os.path.exists(obsidian_file):
            obsidian_dir = current_path
            break
        current_path = os.path.dirname(current_path)
    
    user_vault = vault_path.get().strip()
    if user_vault and os.path.exists(user_vault):
        rating_dir = os.path.join(user_vault, "rating_result")
    elif obsidian_dir:
        rating_dir = os.path.join(obsidian_dir, "rating_result")
    else:
        rating_dir = os.path.join(main_dir, "rating_result")
    
    if not os.path.exists(rating_dir):
        os.makedirs(rating_dir)
    
    if os.name == 'nt':
        subprocess.Popen(f'explorer "{rating_dir}"')
    elif os.name == 'posix':
        subprocess.Popen(['open', rating_dir])

root = tk.Tk()
root.title("Оценка Трека")
root.geometry("600x580")
root.resizable(False, False)

tk.Label(root, text="Название трека:").pack()
track_name = tk.StringVar()
tk.Entry(root, textvariable=track_name, font=("Arial", 14)).pack(fill="x", padx=10, pady=5)

vault_path = tk.StringVar()

slider_frame = tk.Frame(root)
slider_frame.pack(pady=10)
sliders = []
score_var = tk.StringVar()

criteria = [
    ("Рифмы и/или Образы", 10),
    ("Структура и/или Ритмика", 10),
    ("Реализация выбранного стиля", 10),
    ("Индивидуальность и/или Харизма", 10),
    ("Атмосфера и/или Вайб", 5),
    ("Трендовость и/или Популярность", 5),
]

for i, (text, max_val) in enumerate(criteria):
    row = tk.Frame(slider_frame)
    row.pack(fill="x", pady=3)
    tk.Label(row, text=text, width=30, anchor="w").pack(side="left")
    val = tk.IntVar(value=1)
    slider = tk.Scale(row, from_=1, to=max_val, orient="horizontal",
                      variable=val, command=lambda e: update_score(),
                      resolution=1, showvalue=False, length=300)
    slider.pack(side="left", padx=5)
    value_label = tk.Label(row, textvariable=val, width=3)
    value_label.pack(side="right")
    sliders.append(val)

tk.Label(root, textvariable=score_var, font=("Arial", 12, "bold")).pack(pady=15)
score_var.set("Ожидаем оценку...")

button_frame = tk.Frame(root)
button_frame.pack()

tk.Button(button_frame, text="Оценить", font=("Arial", 14), command=calculate_score, bg="#dd4444", fg="white").pack(padx=10)

root.mainloop()
