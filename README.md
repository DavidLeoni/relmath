
Symbolic relational mathematics in Python


1) Install dependencies:


```bash
python3 -m pip install --user -r requirements.txt
```

2) Install Jupyter

3) Install bqplot for Jupyter:

Anaconda:

    conda install -c conda-forge bqplot
    
    (Automatically enables extension in Jupyter)
    Installare bqplot con conda abiliterà automaticamente l’estensione per te in Jupyter

Linux/Mac:

install ipywidgets (--user installs in home):

```bash
python3 -m pip install --user bqplot
```

now enable extension:

```bash
jupyter nbextension enable --py bqplot
```
