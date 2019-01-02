import pytest
from relmath import *

def m0():
    return Rel([[RD(0)]], ['a'], ['x'])


def m1():
    return Rel([[RD(1)]], ['a'], ['x'])

def minus_m1():
    return Rel([[RD(-1)]], ['a'], ['x'])


def m21():
    return Rel([
                [RD(7)],
                [RD(9)]
               ],
               ['a','b'], ['x'])

def m12():
    return Rel([
                [RD(7),RD(9)]
               ], ['x'], ['a','b'])

TEST_GLOBAL_M0 = m0()

class TestState:
     
    def test_quotes(self):
        print(State.s._quotes)

        with quote():
            print(State.s._quotes)
        print(State.s._quotes)

    def test_name(self):
        M1_OUTSIDE_WITH = m1()

        assert '' == State.s.find_expr_name(TEST_GLOBAL_M0)
        assert '' == State.s.find_expr_name(M1_OUTSIDE_WITH)

        with let():
            assert 'TEST_GLOBAL_M0' == State.s.find_expr_name(TEST_GLOBAL_M0)
            assert '' == State.s.find_expr_name(M1_OUTSIDE_WITH)

        with let():
            M0 = m0()
            assert 'M0' == State.s.find_expr_name(M0)
            assert 'M0' == State.s.find_expr_name(TEST_GLOBAL_M0)

            M1 = m1()
            assert 'M1' == State.s.find_expr_name(M1)

        assert '' == State.s.find_expr_name(TEST_GLOBAL_M0)

class TestRD:
    def test_eq(self):
        assert RD(1) == RD(1)
        assert RD(0) != RD(1)

class TestRel:

    def test_dom_dim(self):
        with pytest.raises(ValueError):
            Rel([[RD(1)]], ['a','b'], ['x'])

    def test_cod_dim(self):
        with pytest.raises(ValueError):
            Rel([[RD(1)]], ['a'], ['x', 'y'])

    def test_min_dim_1(self):
        with pytest.raises(ValueError):
            Rel([[]], ['a'], [])

    def test_min_dim_2(self):
        with pytest.raises(ValueError):
            Rel([[], []], ['a','b'], [])

    def test_min_dim_3(self):
        with pytest.raises(ValueError):
            Rel([], [], [])

    def test_list_of_lists(self):
        with pytest.raises(ValueError):
            Rel([(RD(1),RD(2))], ['a','b'], ['x'])

        with pytest.raises(ValueError):
            Rel(([RD(1),RD(2)]), ['a','b'], ['x'])


    def test_eq(self):
        M0 = m0()
        M1 = m1()
        assert M0 == m0()
        assert M1 == m1()
        assert M0 != M1



    def test_val_RD(self):
        assert Rel([[1]],['a'],['x']) == Rel([[RD(1)]],['a'],['x'])
        assert Rel([[1]],['a'],['x']) != Rel([[RD(1)]],['a'],['y'])
        assert Rel([[1]],['a'],['x']) != Rel([[RD(1)]],['b'],['x'])
        assert Rel([[1]],['a'],['x']) != Rel([[RD(0)]],['a'],['x'])

    def test_val_BD(self):
        assert Rel([[False]],['a'],['x']) == Rel([[BD(False)]],['a'],['x'])


    def test_neg(self):
        M1 = m1()
        assert -M1 == minus_m1()

    def test_neg_neg(self):
        M1 = m1()
        assert - (-M1) == m1()

        M12 = m12()
        assert -(-M12) == m12()

        M21 = m21()
        assert -(-M21) == m21()

class TestTranspose:
    def test_T(self):
        M1 = m1()
        M1.T
        assert M1.T.g == m1().g

        M21 = m21()
        assert M21.T == m12()

    def test_simp_T(self):
        M1 = m1()
        with quote():
            M1T = M1.T
        assert M1T.simp().g == m1().g

        M21 = m21()
        with quote():
            M21T = M21.T 
        assert M21T.simp() == m12()


    def test_TT(self):
        M21 = m21()
        assert M21.T.T == m21()

        M12 = m12()
        assert M12.T.T == m12()

    def test_simp_TT(self):
        M21 = m21()
        with quote():
            M21TT = M21.T.T
        assert M21TT.simp() == m21()

        M12 = m12()
        with quote():
            M12TT = M12.T.T
        assert M12TT.simp() == m12()


class TestMul:

    def test_id(self):
        M1 = m1()
        M1p = m1()
        M1r = m1()
        assert round(M1 * M1p, 7) == round(M1r, 7)

    def test_zero_10(self):
        M1 = m1()
        M0 = m0()
        Mr = m0()
        assert round(M1 * M0, 7) == round(Mr, 7)
    def test_zero_01(self):
        
        M1 = m1()
        M0 = m0()
        Mr = m0()
        assert round(M0 * M1, 7) == round(Mr, 7)

    def test_m21_id(self):
        
        M12 = m21()
        M1 = m1()
        Mr = m21()
        assert round(M12 * M1, 7) == round(Mr, 7)

    def test_m12_m21(self):
        
        M12 = m12()
        M21 = m21()
        Mr = Rel([[M12.g[0][0]*M21.g[0][0]+ M12.g[0][1]*M21.g[1][0] ]],M12.dom, M21.cod)
        assert round(M12 * M21, 7) == round(Mr, 7)


def pexpr(msg, expr):
    info("python:  %s" % msg)
    info('repr:    %r ' % expr) 
    info('str:\n%s' % str(expr))

def test_trial():
    M = Rel([[RD(9),RD(0), RD(6)], [RD(0),RD(5), RD(7)]], ['a','b'], ['x','y','z'])
    U = Rel([[RD(9),RD(0), RD(6)], [RD(0),RD(5), RD(7)]], ['a','b'], ['x','y','z'])

    print(-Rel([[RD(1)]],['a'],['x']) == Rel([[RD(-1)]],['a'],['x']))

    pexpr('M.T', M.T)
    with quote():
        pexpr('M.T', M.T)
    pexpr('U.T', U.T)
    with quote():
        pexpr('U.T', U.T)


    pexpr('M', M)

    with quote():
        pexpr('M.T', M.T)
    pexpr('-M', -M)
    with quote():    
        pexpr('-M', -M)

    E = RelMul(M, T(M))
    pexpr('M*M.T', (M*M.T))
    with quote():
        pexpr('M*M.T', (M*M.T))

    pexpr("RelMul(M, T(M))", RelMul(M, T(M)))
    with quote():
        pexpr("RelMul(M, T(M))", RelMul(M, T(M)))

    pexpr("RelMul(M, T(M)).simp()" , RelMul(M, T(M)).simp())
    with quote():
        pexpr("RelMul(M, T(M)).simp()" , RelMul(M, T(M)).simp())

    print(sjoin("ciao\npippo", "hello\ndear\nworld"))

    print(sjoin("ciao\npippo", "hello\ndear\nworld\nciao\nmondo\nche\nbello", valign='center'))


    with quote():    
        pexpr('-U' , -U)

    with quote():    
        pexpr('U.T',  U.T)

    pexpr("RelMul(M, T(M))" , RelMul(M, T(M)))

    pexpr(" -Rel([[RD(1)]],['a'],['x'])",  -Rel([[RD(1)]],['a'],['x']))


def test_scopes():

    def f():
        x = 'a'
        debug('locals in f %s' % locals())
        debug('z in f globals? %s' %  'z' in globals())
        g()

    def g():
        y = 'b'
        debug('locals in g %s' % locals())
        debug('x in g globals? %s' % 'x' in globals())
       
    z = 'c'
    debug('locals in root %s' % locals())
    debug('z in root globals ? %s' % 'z' in  globals())
    f()    

    with quote():
        locs = locals()
        debug('u in locals() %s' % ('u' in locs))
        u = 'w'
        debug('u in locs %s' % ('u' in locs))
        debug('u in locals() %s' % ('u' in locals()))

def global_fun():
    with let():
        b5 = 'b5'
        debug("State.s.local_vars() = %s" % State.s.local_vars())
        b6 = 'b6'
        debug("State.s.local_vars() = %s" % State.s.local_vars())
    

def test_scopes_let():
    with let():
        b1 = 'b1'
        debug("State.s.local_vars() = %s" % State.s.local_vars())
        b2 = 'b2'
        debug("State.s.local_vars() = %s" % State.s.local_vars())

        with let():
            b3 = 'b3'
            debug("State.s.local_vars() = %s" % State.s.local_vars())
            b4 = 'b4'
            debug("State.s.local_vars() = %s" % State.s.local_vars())
            global_fun()
    
test_scopes_let()

test_trial()