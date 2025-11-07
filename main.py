import tkinter as tk
from ui.page_systeme_lineaire import PageSystemeLineaire
from ui.page_regression_lineaire import PageRegressionLineaire
from ui.page_programmation_lineaire import PageProgrammationLineaire


class App(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Modelisation Mathematique")
        self.geometry("800x500")

        container = tk.Frame(self)
        container.pack(fill="both", expand=True)

        # Pour la navigation dans l'app
        sidebar = tk.Frame(container, width=200, bg="#2c3e50")
        sidebar.pack(side="left", fill="y")

        # Zone pour afficher les pages
        self.content = tk.Frame(container, bg="#f1efec")
        self.content.pack(side="right", fill="both", expand=True)

        # Instancier chaque page dans un dictionnaire
        self.frames = {}
        for F in (PageSystemeLineaire, PageRegressionLineaire, PageProgrammationLineaire):
            page_name = F.__name__
            frame = F(self.content, self)
            self.frames[page_name] = frame
            frame.grid(row=0, column=0, sticky="nsew")

        tk.Label(sidebar, text="ModMaths", font=("Arial", 16)).pack(fill="x", pady=26, padx=10)

        btn1 = tk.Button(sidebar, text="Systeme Lineaire",
                         command=lambda: self.show_frame("PageSystemeLineaire"),
                         bg="#34495e", fg="white", relief="flat")
        btn1.pack(fill="x", pady=5, padx=10)

        btn2 = tk.Button(sidebar, text="Regression Lineaire",
                         command=lambda: self.show_frame("PageRegressionLineaire"),
                         bg="#34495e", fg="white", relief="flat")
        btn2.pack(fill="x", pady=5, padx=10)

        btn3 = tk.Button(sidebar, text="Programmation Lineaire",
                         command=lambda: self.show_frame("PageProgrammationLineaire"),
                         bg="#34495e", fg="white", relief="flat")
        btn3.pack(fill="x", pady=5, padx=10)

        self.show_frame("PageRegressionLineaire")

    # Pour afficher une page
    def show_frame(self, page_name):
        frame = self.frames[page_name]
        frame.tkraise()


if __name__ == "__main__":
    app = App()
    app.mainloop()
