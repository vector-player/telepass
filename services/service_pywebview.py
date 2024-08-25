def display_html_string(html_string, header:str="", on_top:bool=True):
    try:
        import webview
        webview.create_window(header, html=html_string, on_top=on_top, background_color='#FFFFFF',)
        webview.start()
        # webview.start(block=False)
    except Exception as e:
        print(e)

def display_html_online(url, header:str="", on_top:bool=True, background_color='#FFFFFF',):
    try:
        import webview
        webview.create_window(header, url, on_top=on_top)
        webview.start()
        # webview.start(block=False)
    except Exception as e:
        print(e)