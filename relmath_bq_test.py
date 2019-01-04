from relmath import *
from relmath_bq import *

doms =  [
            ['a','b','c'],
            ['x','y','z','w'],
            ['g','h']
        ]
labels = ['M1', 'M2', 'M3']
edges = [
            [
                [3,2,5,6],
                [6,2,3,8],
                [1,4,5,2]
            ],
            [
                [4,5],
                [6,2],
                [9,1],
                [8,6],
            ],
        ]

def try_mul():

    with quote():
        with let():
            M = Rel([
                        [0.2, 0.7, 0, 0],
                        [0.9,0,0.5,0],
                        [0.9,0,0,0]
                    ], 
                    ['a','b','c'], 
                    ['x','y','z','w'])        
            E = M * M.T
        
            print(E)
            print(E.simp())
            return E.to_bq()

try_mul()