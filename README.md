
# 🗂️ File Manager — Streamlit CRUD App

A small, secure file management UI built with Streamlit. Supports Create, Read, Update, and Delete operations on text files — all safely sandboxed to a local workspace folder.

## 🔗 Live Demo
[View Live App](#) <!-- replace # with your Streamlit Cloud URL once deployed -->

## ✨ Features
- **Browse** — view all files in the workspace with size and last-modified timestamp
- **Create** — add new text files with custom content
- **Read** — view file contents and download them
- **Update** — rename, append to, or overwrite existing files
- **Delete** — remove files with a confirmation checkbox

## 🔒 Security
All user-supplied filenames are stripped of path components before use, preventing directory traversal (e.g. `../../etc/passwd`) or absolute path access. Every operation is strictly confined to the `file_manager_workspace/` folder.

## 🛠️ Tech Stack
- Python
- Streamlit
- pathlib

## 🚀 Run Locally
```bash
git clone https://github.com/ferroxcreation009-hub/File-Manager-Streamlit.git
cd File-Manager-Streamlit
pip install streamlit
python -m streamlit run app.py
```

## 👤 About Me
Built by Ankush Khan — incoming B.Tech CSE (AI/ML) student, self-taught in web development.

- 🔗 LinkedIn: [linkedin.com/in/ankush-khan-6a6219411](https://www.linkedin.com/in/ankush-khan-6a6219411/)
- 💻 GitHub: [@ferroxcreation009-hub](https://github.com/ferroxcreation009-hub)
