# Introduction
Procedurally generated animation of the anti-twister mechanism and its connection to Spin(3).
Also known as Dirac's belt trick, a demonstration of an object that is subject to $4\pi$ or $720°$ symmetry, so it needs two full revolutions to revert to its initial state.

Inspired by Jason Hise's animations, please check out:
https://en.wikipedia.org/wiki/User:JasonHise

![Observables as quaternions](https://raw.githubusercontent.com/AmirLeidel/spinny/master/diagram1.png)
*States of the anti-twister and their corresponding spin observables as quaternions*

# How it works
Coded using conformal geometric algebra motor interpolation as described by Belon et al (2017).

In order to model the ribbon in $s$-direction while rotating in $r$. We define three oriented control points using CGA rotors. 
For this, using two rotors $R$ and $S$, describing the rotation of the center cube and the twisting of the ribbon
$$ R = \exp(\frac{r}{e_{123}} \pi \lambda),$$
$$ S = \exp(-\frac{s}{e_{123}} \frac{\pi}{2})$$
and three translators
$$ T_0 = 1- \frac{R(\lambda) 0.3 s R(\lambda)^\dagger \wedge e_\infty}{2},$$
$$ T_1 = 1- \frac{R(\lambda) 1.0 s R(\lambda)^\dagger \wedge e_\infty}{2},$$
$$ T_2 = 1- \frac{2.0 s \wedge e_\infty}{2} $$
we define the oriented control points as
$$ M_0 = T_0 R S $$
$$ M_1 = T_1 R S $$
$$ M_2 = T_2 $$
Which can be interpolated by motor logarithms:
$$ M = \exp(\sum_i B_i(\alpha) \log(M_i(\lambda)))$$


References:

[1] Belon, M.C.L., Hildenbrand, D. Practical Geometric Modeling Using Geometric Algebra Motors. Adv. Appl. Clifford Algebras 27, 2019–2033 (2017). https://doi.org/10.1007/s00006-017-0777-z
