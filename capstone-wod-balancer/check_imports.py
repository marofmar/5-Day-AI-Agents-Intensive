import sys
print(sys.executable)
try:
    import dotenv
    print(f"dotenv: {dotenv.__file__}")
    import markdown
    print(f"markdown: {markdown.__file__}")
    import xhtml2pdf
    print(f"xhtml2pdf: {xhtml2pdf.__file__}")
except ImportError as e:
    print(e)
