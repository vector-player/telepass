# import sys
## append package-root to sys, so modules in package could be recognized and imported
# sys.path.append("<path/to/package/root/dir>")
# from python_pywebview_standalone import webview
# from ..pywebview_standalone import webview


def display_html_string():
    import webview
    webview.create_window('Hello world', html="<h1>h1</h1><h2>h2</h2>")
    webview.start()


def display_html_online():
    import webview
    webview.create_window('Hello world', 'https://telepass.app/')
    webview.start()