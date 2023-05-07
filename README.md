# Introduction
Procedurally generated animation of the anti-twister mechanism and its connection to Spin(3).
Also known as Dirac's belt trick, a demonstration of an object that is subject to $4\pi$ or $720°$ symmetry, so it needs two full revolutions to revert to its initial state.

Inspired by Jason Hise's animations, please check out:
https://en.wikipedia.org/wiki/User:JasonHise

![Observables as quaternions](https://raw.githubusercontent.com/AmirLeidel/spinny/master/diagram1.png)
*States of the anti-twister and their corresponding spin observables as quaternions*

# How it works
Coded using conformal geometric algebra motor interpolation as described by Belon et al (2017).

In order to model the ribbon that is secured in $s$-direction while rotating in $r$ by $2\pi\lambda \mathrm{rad}$. We define three oriented control points using CGA rotors. 
For this, using two rotors $R$ and $S$, describing the rotation of the center cube and the twisting of the ribbon
$$R(\lambda) = \exp(\frac{r}{e_{123}} \pi \lambda),$$
$$S(\lambda) = \exp(-\frac{s}{e_{123}} \frac{\pi}{2})$$
and three translators
$$T_0(\lambda) = 1- \frac{R(\lambda) 0.3 s R(\lambda)^\dagger \wedge e_\infty}{2},$$
$$T_1(\lambda) = 1- \frac{R(\lambda) 1.0 s R(\lambda)^\dagger \wedge e_\infty}{2},$$
$$T_2 = 1- \frac{2.0 s \wedge e_\infty}{2} $$
we define the motors of oriented control points as
$$M_0(\lambda) = T_0(\lambda) R(\lambda) S(\lambda) $$
$$M_1(\lambda) = T_1(\lambda) R(\lambda) S(\lambda) $$
$$M_2(\lambda) = T_2 $$
Which can be interpolated by motor logarithms:
$$M(\lambda,\alpha) = \exp(\sum_i B_i(\alpha) \log(M_i(\lambda)))$$
Where $\alpha \in \left[0,1\right]$ is the interpolation parameter along the ribbon originating from the center cube face. And $B_i(\alpha)$ are weight functions defined using
$$B_1'(\alpha) = (1-\alpha)^2,$$
$$B_2'(\alpha) = 10 \alpha^2 (1-\alpha)^4,$$
$$B_3'(\alpha) = \alpha^3$$
which are normalized by defining $B_i(\alpha) = B_i(\alpha) / \sum_j B_j'(\alpha)$.

Finally, the interpolation motor $M(\lambda,\alpha)$ can be used to calculate the mesh of a ribbon extending in $c$ direction 
$$ \rho_{l,r}(\lambda,\alpha) = M(\lambda,\alpha) (\pm c) M(\lambda,\alpha)^\dagger.$$
Where $\rho_{l}(\lambda,\alpha)$ and $\rho_{r}(\lambda,\alpha)$ are the left and right boundaries respectively.

References:

[1] Belon, M.C.L., Hildenbrand, D. Practical Geometric Modeling Using Geometric Algebra Motors. Adv. Appl. Clifford Algebras 27, 2019–2033 (2017). https://doi.org/10.1007/s00006-017-0777-z
