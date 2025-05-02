# 📝 To-Do List App

A feature-rich command-line **To-Do List app** written in Python.

---

## ✨ Features

✅ Add tasks with names, deadlines, and priorities
✅ View tasks with checkboxes, deadlines, and priority indicators
✅ Edit tasks: change name, deadline, priority
✅ Sort tasks:
- Alphabetically
- By earliest deadline
- By highest priority
✅ Mark tasks as done
✅ Reorder tasks manually
✅ Save and load tasks using a `.pkl` file (planned upgrade to JSON/CSV)
✅ Colorful UI using `colorama`
✅ ASCII art logo + motivational quotes
✅ Clear, user-friendly menus

---

## 📦 Planned Features

🚀 Settings menu:
- Change color theme
- Toggle saving on/off
- Export data to JSON, CSV, or TXT
- Add categories/tags

---

## ⚙ Installation

1. Clone the repository:
```bash
git clone https://github.com/yourusername/to_do_list.git

2. Install dependencies:
pip install colorama

3. Run the app:
python to_do_list.py

---

## 💡 How It Works
Tasks are stored as dictionaries with name, deadline, and priority keys.

Data is saved in a .pkl file for persistence.

Colorful CLI interface built with colorama.

Clear separation of features (add, delete, edit, sort, etc.) into functions.

## 📅 Development Log (Highlights)
25/02/2025: Complete rewrite for user-friendliness

27/02/2025: Added save/load and clear terminal

28/02/2025: Improved removing by index and UI design

29/04/2025: Better error handling and global state handling

01/05/2025: Added color themes and deadlines

02/05/2025: Added sorting and improved deadline/priority input

## 🙏 Credits
Core design and development: Jacob Britus

Assisted by ChatGPT for research and improvements


## 🔖 License
This project is licensed under the MIT License.