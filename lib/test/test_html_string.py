"""
module to test tkhtmlview with html string
"""

import tkinter as tk
from tkhtmlview_p import HTMLLabel

root = tk.Tk()
html_label = HTMLLabel(
    root,
    html='<h1 style="color: red; text-align: center"> Hello World </H1>'
)
html_label.pack(fill="both", expand=True)
html_label.fit_height()
root.mainloop()
