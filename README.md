
Symbolic relational mathematics in Python, mainly for didactical purposes 

**STATUS**: Planning (Jan 2019) - don't bother to download

## Philosophy:

Data science is full of matrices, but few really understand why.

Everything is a graph, with nodes and edges joining them (i.e. people are nodes and 'friend-of' a relation between them)

A graph can be represented by a matrix. 

Operations on matrices are all about linear algebra, which is a high-school subject but is often perceived as mysterious

Operation on graphs are all about graph algorithms, which are often highly optimized but hard to understand

Visualizing graphs is easier then visualizing matrices

Operations on matrices -> operations on graphs and viceversa

**Conclusion**: if we visualize operations on matrices as graphs we can get insights both about linear algebra and graph theory.

## Goals

1. as simple and direct as possible
2. must favor exeprimentation with interactive graphical widgets 
3. take best ideas from existing projects, such as sympy and term rewriting as done in rubi integrator

## Non-goals

1. performance: tool is mainly for didactical purposes)
2. comprehensiveness: there are already several tools for symbolic math, se we keep scope limited to matrix operations

## Implementation

1. python 3 library [relmath.py](relmath.py)
2. separate viz library [relmath_bq.py](relmath_bq.py) for interactive widgets to be shown in jupyter worksheets with bqplot
3. decent testing with [pytest](https://docs.pytest.org/en/latest/) and (in the future) [Hypothesis](https://hypothesis.readthedocs.io)
4. all data is immutable
5. occasionally we do allow monkey patching and ugly stuff


## Installation

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
