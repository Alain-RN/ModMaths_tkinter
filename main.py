import tkinter as tk
from ui.page_systeme_lineaire import PageSystemeLineaire
from ui.page_regression_lineaire import PageRegressionLineaire
from ui.page_programmation_lineaire import PageProgrammationLineaire


class App(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Modelisation Mathematique")
        self.geometry("846x580")
        self.resizable(False, False)

        container = tk.Frame(self)
        container.pack(fill="both", expand=True)

        # Pour la navigation dans l'app
        sidebar = tk.Frame(container, width=224, bg="#2c3e50")
        sidebar.pack(side="left", fill="y")
        sidebar.pack_propagate(False)

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

        tk.Frame(sidebar, height=10, bg="#2c3e50").pack()
        
        tk.Label(
            sidebar, text="m o d M a t h s", font=("Arial", 13, "bold"), fg="white",
            pady=14.5, background="#32475c"
        ).pack(fill="x", pady=30, padx=20)

        tk.Frame(sidebar, height=4, bg="#2c3e50").pack()

        btn1 = tk.Button(
            sidebar, text="Systeme Lineaire", font=("Arial", 10, "bold"),
            command=lambda: self.show_frame("PageSystemeLineaire"),
            bg="#34495e", fg="white", relief="flat",
            pady=5
        )
        btn1.pack(fill="x", pady=0, padx=20)

        btn2 = tk.Button(
            sidebar, text="Regression Lineaire", font=("Arial", 10, "bold"),
            command=lambda: self.show_frame("PageRegressionLineaire"),
            bg="#34495e", fg="white", relief="flat",
            pady=5
        )
        btn2.pack(fill="x", pady=16, padx=20)

        btn3 = tk.Button(
            sidebar, text="Programmation Lineaire", font=("Arial", 10, "bold"),
            command=lambda: self.show_frame("PageProgrammationLineaire"),
            bg="#34495e", fg="white", relief="flat",
            pady=5
        )
        btn3.pack(fill="x", pady=0, padx=20)

        self.show_frame("PageProgrammationLineaire")

    # Pour afficher une page
    def show_frame(self, page_name):
        frame = self.frames[page_name]
        frame.tkraise()


if __name__ == "__main__":
    app = App()
    app.mainloop()
