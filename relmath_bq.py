import numpy as np
from bqplot import *
from bqplot.marks import Graph
from ipywidgets import Layout, VBox, HBox
from relmath import * 


def Rel_bq_npartite(rel_exprs):
    """ 
            M1      M2     M3
        a  ---- x ----- p --- g
        b  -----y     _-q --- h
        c  -----z ---/      
                w

                M1*M1*M3
        a ------------------- g
        b                 _-- h
        c ---------------/
    """    
    if len(rel_exprs) == 0:
        raise ValueError("Expected a non-empty list !")
    i = 0
    for expr in rel_exprs:
        if not isinstance(expr, Expr):
            raise ValueError("Expected an Expr ! Instead Found as value at index %s this  %s " % (i,expr))
        i += 1

    

    """
        node_data = [
            {'label': 'A', 'shape': 'circle', 'shape_attrs': {'r': 20}, 'foo': 1},
            {'label': 'Node B', 'shape': 'rect', 'shape_attrs': {'rx': 10, 'ry': 10, 'width': 40}, 'foo': 2},
            {'label': 'C', 'shape': 'ellipse', 'foo': 4},
            {'label': 'D', 'shape': 'rect', 'shape_attrs': {'width': 30, 'height': 30}, 'foo': 100},
        ]    
    """

    texts = []
    node_data = []    
    link_data = []
    x = []
    y = []

    base = 0
    x_distance = 100
    # fake rel
    
    for rel in rel_exprs :
        srel = rel.simp()
        n = len(srel.dom)
        m = len(srel.cod)
        for i in range(n):
            for j in range(m):
                link_data.append({'source': base + i, 'target': base + n + j, 'value': srel.g[i][j].val})
        base += n
    
    aug_rel_exprs = rel_exprs + [rel_exprs[-1].simp().T]
    
    ry = 15
    max_d_len = 2
    for rel in aug_rel_exprs:
        for d in srel.dom:
            max_d_len = max(len(d), max_d_len)
    rx = max_d_len * 5
    if max_d_len > 2:
        node_data_template = {  'shape' : 'ellipse', 
                                # 'shape_attrs': {'rx': max_d_len * 7, 'ry': 10, 'width': 40}
                                'shape_attrs': {'width': rx, 'height': ry + ry // 2},
                                'shape_attrs': {'rx': rx, 'ry': ry}
                             }
    else: 
        node_data_template = {'shape' : 'circle', 'shape_attrs': {'r': ry + ry // 2}}


    i = 0
    for rel in aug_rel_exprs:
        srel = rel.simp()
        # note: requires python 3.5
        node_data.extend([{**node_data_template, 'label':d} for d in srel.dom])
        n = len(srel.dom)
        
        x.extend(([(i+1)*x_distance] * n))
        y.extend((ky for ky in reversed(range(n))))

        if i < len(rel_exprs):
            with quote():
                texts.append(str(rel))

        i += 1

    #fig_layout = Layout(width='960px', height='600px')
    
    xs = LinearScale()
    ys = LinearScale()
    lcs = ColorScale(scheme='Reds')
    
    labels = Label(x=[(i*x_distance) + (x_distance/2) for i in range(1, len(rel_exprs)+1)],
                   y=[max(y)+1]*2, scales={'x': xs, 'y': ys},
                text=texts, default_size=26, font_weight='bolder',
                colors=['black'], update_on_move=True)
    

    """
            self.graph.hovered_style = {'stroke': '1.5'}
            self.graph.unhovered_style = {'opacity': '0.4'}
            
            self.graph.selected_style = {'opacity': '1',
                                        'stroke': 'red',
                                        'stroke-width': '2.5'}

    """

    graph = Graph(  node_data=node_data, link_data=link_data, link_type='line',
                    colors=['orange'], directed=False, 
                    scales={'x': xs, 'y': ys, 'link_color': lcs}, 
                    x=x, y=y,  color=['black']*len(node_data))

    #return Figure(marks=[graph, labels], layout=fig_layout)    
    #fig_layout = Layout(width='960px', height='600px')
    return Figure(marks=[graph, labels])    




def BinOp_to_bq(self):

        fig1 = Rel.bq_npartite([self.left, self.right])
        fig2 = Rel.bq_npartite([self])    
        
        return VBox([fig1, fig2])
        

# monkey patching
Rel.bq_npartite = Rel_bq_npartite
BinOp.to_bq = BinOp_to_bq
