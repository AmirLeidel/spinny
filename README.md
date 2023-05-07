# Introduction
Procedurally generated animation of the anti-twister mechanism and its connection to Spin(3).
Also known as Dirac's belt trick, a demonstration of an object that is subject to $4\pi$ or $720°$ symmetry, so it needs two full revolutions to revert to its initial state.

Inspired by Jason Hise's animations, please check out:
https://en.wikipedia.org/wiki/User:JasonHise

![Observables as quaternions](https://raw.githubusercontent.com/AmirLeidel/spinny/master/diagram1.png)
*States of the anti-twister and their corresponding spin observables as quaternions*

# How it works
Coded using conformal geometric algebra motor interpolation as described by Belon et al (2017).

We define three oriented control points using the CGA rotors 
$$
a^2+b^2+c^2 
=abc
$$


References:

Belon, M.C.L., Hildenbrand, D. Practical Geometric Modeling Using Geometric Algebra Motors. Adv. Appl. Clifford Algebras 27, 2019–2033 (2017). https://doi.org/10.1007/s00006-017-0777-z
