
# RelMath theory 

## On rule-based transformations

Rubi integrator is an interesting project for symbolic math

Highlights from paper:
http://www.apmaths.uwo.ca/~arich/A%20Rule-based%20Knowledge%20Repository.pdf

- Define Functionally.
- Restrict to domains of validity. 
- Restrict to simplification. To avoid infinite loops, applications of rules must eventually result in an
expression that can be made no simpler (i.e. an expression to which no rules applies). The conditions
attached to a rule must limit its application to those expressions for which its application results in a
simpler expression.
- Provision for local variables
- **Mutually exclusive**  For a  collection of transformation rules  to be properly defined, at most  one  of the rules can be applicable to any given expression. __Mutual exclusivity is critical to ensuring that
rules can be added, removed or modified without affecting the other rules__. Such stand-alone, order-
independent rules make it possible to build a rule-based repository of knowledge incrementally and
as a collaborative effort.


– Integration formulas give final results; Rule collections may not.

## co-occurrance matrices

* Nees Jan van Eck andLudo Waltman [How to Normalize Co-Occurrence Data? An Analysis of Some Well-Known Similarity Measures](https://repub.eur.nl/pub/14528/ERS-2009-001-LIS.pdf)
* Loet Leydesdorff [Should Co-occurrence Data be Normalized?](https://www.leydesdorff.net/coocc07/)