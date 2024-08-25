"""
module to test tkhtmlview with existing html file
"""

import sys
import os
# import tkinter
from telepass.lib import tkinter as tk
from ..tkhtmlview import HTMLText, RenderHTML
sys.path.append(os.path.dirname(os.path.realpath(__file__)))

def render_index():
    root = tk.Tk()
    html_label = HTMLText(root, html=RenderHTML('index.html'))
    html_label.pack(fill="both", expand=True)
    html_label.fit_height()
    root.mainloop()

if __name__ == "__main__":
    render_index()