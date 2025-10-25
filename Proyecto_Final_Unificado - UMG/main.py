
import os, sys, subprocess, tkinter as tk

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

SEARCH_SPEC = {
    "Álgebra Lineal": {
        "filenames": ["App_Algebra.py", "app_algebra.py"],
        "prefer_dir_keys": ["algebra", "álgebra", "lineal"]
    },
    "Algoritmos": {
        "filenames": ["app.py"],
        "prefer_dir_keys": ["algoritmo", "algoritmos", "algorit"]
    },
    "Matemática Discreta": {
        "filenames": ["app_mate_discreta.py", "app_mate_discreta"],
        "prefer_dir_keys": ["discreta", "discreto", "matematica", "matemática"]
    },
}

def find_candidates(root, max_depth=4):
    out = []
    for cur, dirs, files in os.walk(root):
        rel = os.path.relpath(cur, root)
        depth = 0 if rel == "." else len(rel.split(os.path.sep))
        if depth > max_depth:
            dirs[:] = []
            continue
        low_dir = cur.lower()
        for f in files:
            out.append((os.path.join(cur, f), os.path.relpath(os.path.join(cur, f), root), depth, low_dir))
    return out

def select_entry(subject):
    spec = SEARCH_SPEC[subject]
    target = set(n.lower() for n in spec["filenames"])
    keys = [k.lower() for k in spec["prefer_dir_keys"]]
    cands = []
    for path, rel, depth, low_dir in find_candidates(BASE_DIR):
        name = os.path.basename(path).lower()
        if name in target:
            score = 100 - depth * 10
            if any(k in low_dir for k in keys):
                score += 50
            parent = os.path.basename(os.path.dirname(path)).lower()
            if any(k in parent for k in keys):
                score += 30
            cands.append((score, path))
    if not cands:
        return None
    cands.sort(key=lambda x: -x[0])
    return cands[0][1]

def launch(path, subject):
    import tkinter.messagebox as messagebox
    if not path or not os.path.isfile(path):
        msg = f"No pude localizar el archivo de entrada para {subject}.\n"
        if path:
            msg += f"Ruta tentativa: {path}\n"
        req = ', '.join(SEARCH_SPEC[subject]['filenames'])
        msg += f"Se espera uno de: {req}"
        messagebox.showerror("Proyecto no encontrado", msg)
        return
    try:
        cwd = os.path.dirname(path)
        subprocess.Popen([sys.executable, path], cwd=cwd)
    except Exception as e:
        messagebox.showerror("Error al iniciar", f"No se pudo ejecutar:\n{path}\n\n{e}")

def main():
    resolved = {s: select_entry(s) for s in SEARCH_SPEC.keys()}

    root = tk.Tk()
    root.title("Menú Principal — Proyectos (Tkinter)")
    root.geometry("520x360")
    root.configure(bg="#0f172a")

    title = tk.Label(root, text="Menú Principal", font=("Segoe UI", 18, "bold"), fg="#e2e8f0", bg="#0f172a")
    subtitle = tk.Label(root, text="Selecciona una materia para abrir su proyecto", font=("Segoe UI", 11), fg="#94a3b8", bg="#0f172a")
    title.pack(pady=(24,4))
    subtitle.pack(pady=(0,16))

    frame = tk.Frame(root, bg="#0f172a")
    frame.pack(expand=True, fill="both", padx=20, pady=10)

    order = ["Matemática Discreta","Algoritmos","Álgebra Lineal"]
    for subj in order:
        tk.Button(frame, text=subj, font=("Segoe UI", 12, "bold"),
                  command=lambda s=subj: launch(resolved.get(s), s),
                  bg="#2563eb", fg="white", activebackground="#1d4ed8", activeforeground="white",
                  relief="raised", bd=2, padx=12, pady=12, cursor="hand2", wraplength=380, justify="center").pack(fill="x", pady=8)


    root.mainloop()

if __name__ == "__main__":
    main()
