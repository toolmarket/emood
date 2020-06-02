Emood
--------

Esto es un documento temporal con datos.

https://github.com/toolmarket/emood


TO DO
-----
**New Dev**
1. Save Answers.
2. Loop ping.
3. Loop show smiles.
4. Loop send answers. 



# Agregar a "autoinicio" >> Esto lo hace el Instalador
https://hackernoon.com/the-one-stop-guide-to-easy-cross-platform-python-freezing-part-1-c53e66556a0a. o tratar de hacer un shortcut como hace AHK sin admin. 
https://python-packaging.readthedocs.io/en/latest/index.html
https://pyinstaller.readthedocs.io/en/stable/

# Instaladores "Cross platform"
https://www.almtoolbox.com/install-builder.php#installanywhere
http://izpack.org/downloads/

# Instalador Windows
https://jrsoftware.org/isdl.php


REMEMBER
--------
- Users will have an INBOX on the DB, where admins can queue up actions. 

-------------------------------------------------------

# Create empty Virtualenv https://stackoverflow.com/questions/58000371/how-to-create-an-empty-python-virtual-environment
# pip freeze > requirements.txt
# pip install -r requirements.txt
env\Scripts\activate.bat 

Problema con MAC, debe ser por esto:
------------------------------------
pip3 install setuptools==45.0.0 # para Mac
https://pypi.org/project/mac-login-items/
https://stackoverflow.com/questions/32078005/using-python-and-tkinter-to-make-a-simple-gui-i-get-unrecognized-selector-sent
https://www.python.org/download/mac/tcltk/
import pkg_resources
print('Hello')


pip install requests pystray


# COMPILAR
pip install https://github.com/pyinstaller/pyinstaller/archive/develop.zip
pyinstaller main.py --windowed

https://pyinstaller.readthedocs.io/en/stable/usage.html
pyinstaller emood/emood.py -n emood --noconfirm --add-data emood/src:dist/emood

# OPCION 2 COMPILAR>
https://cx-freeze.readthedocs.io/en/latest/overview.html






Buen ejemplo a seguir:
https://github.com/metabrainz/picard




Si no embedder el python.exe y listo. 