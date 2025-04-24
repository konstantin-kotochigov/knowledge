# Characterisrtic Function

Suppose we have PDF $f_{\zeta}(x)$ for some variable $\zeta$<br>
We can construct version of this function called characteristic function

$$\phi(t) = E[e^{i t \zeta}] = \int_{-\inf}^{\inf} e^{itX} f(X) dx$$

Based on the definition it is just a __Fourrier transform__ of a PDF function<br>


## Fourrier Transform

Recall that Fourrier transform maps any function $f$ to its unique counterpart $\varphi$ in complex domain by cointegratring it with sigmoids $e^{-itx}$ of each frequency $t$. It acts as a mapper from time domain $x$ to frequency domain $t$

The result of complex integration looks like:

$$\varphi(t) = \bigg[\int f(x) \cos(tx) \,dx;  - \int f(x) \sin(tx) \,dx\bigg]$$

This value encodes two pieces of information:
- magnitude of the frequency
- phase information
    - high __Real__ part = captured an even component
    - high __Imaginary__ part = captured an odd component



### Usage

Often used to prove convergence<br>
For example, __CLT:__ the sum of standardized i.i.d random variables converges to N(0,1)


### Moments generation


All distribution moments can be calculated as derivatives of $\phi(t)$<br>$\frac{\partial \varphi}{\partial}$<br><br>

### Properties
Since there is exponent inside the integral sum of the argmunets change to mulitplication<br> $\varphi(X+Y) = \varphi(X) \cdot \varphi(Y)$

