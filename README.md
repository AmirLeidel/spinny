# Introduction
Procedurally generated animation of the anti-twister mechanism and its connection to Spin(3).
Also known as Dirac's belt trick, a demonstration of an object that is subject to $4\pi$ or $720°$ symmetry, so it needs two full revolutions to revert to its initial state.

Inspired by Jason Hise's animations, please check out:
https://en.wikipedia.org/wiki/User:JasonHise

![Observables as quaternions](https://raw.githubusercontent.com/AmirLeidel/spinny/master/diagram1.png)
*States of the anti-twister and their corresponding spin observables as quaternions*

# How it works
Coded using CGA motor interpolation as described by Belon et al (2017).

In order to model the ribbon that is secured in $s$-direction while rotating in $r$ by $2\pi\lambda \mathrm{rad}$. We define three oriented control points using CGA rotors. 
For this, using two rotors $R$ and $S$, describing the rotation of the center cube and the twisting of the ribbon
$$\large R(\lambda) = \exp(\frac{r}{e_{123}} \pi \lambda),$$
$$\large S(\lambda) = \exp(-\frac{s}{e_{123}} \frac{\pi}{2})$$
and three translators
$$\large T_0(\lambda) = 1- \frac{R(\lambda) 0.3 s R(\lambda)^\dagger \wedge e_\infty}{2},$$
$$\large T_1(\lambda) = 1- \frac{R(\lambda) 1.0 s R(\lambda)^\dagger \wedge e_\infty}{2},$$
$$\large T_2 = 1- \frac{2.0 s \wedge e_\infty}{2} $$
we define the motors of oriented control points as
$$\large M_0(\lambda) = T_0(\lambda) R(\lambda) S(\lambda) $$
$$\large M_1(\lambda) = T_1(\lambda) R(\lambda) S(\lambda) $$
$$\large M_2(\lambda) = T_2 $$
Which can be linear-interpolated using motor logarithms:
$$\large M(\lambda,\alpha) = \exp(\sum_i B_i(\alpha) \log(M_i(\lambda)))$$
Where $\alpha \in \left[0,1\right]$ is the interpolation parameter along the ribbon originating from the center cube face. And $B_i(\alpha)$ are weight functions defined using
$$\large B_1'(\alpha) = (1-\alpha)^2,$$
$$\large B_2'(\alpha) = 10 \alpha^2 (1-\alpha)^4,$$
$$\large B_3'(\alpha) = \alpha^3$$
which are normalized by defining $B_i(\alpha) = B_i(\alpha) / \sum_j B_j'(\alpha)$.

Finally, the interpolation motor $M(\lambda,\alpha)$ can be used to calculate the mesh of a ribbon extending in $c$ direction 
$$\large \rho_{l,r}(\lambda,\alpha) = M(\lambda,\alpha) (\pm c) M(\lambda,\alpha)^\dagger.$$
Where $\rho_{l}(\lambda,\alpha)$ and $\rho_{r}(\lambda,\alpha)$ are its left and right boundaries respectively.

The full set of twelve equations (2 boundaries $\times$ 6 directions) for rotating in the $z$-axis is given by
$$\large \rho^{+ x}_{l,r}(\lambda,\alpha) = \underline{M(\lambda, \alpha,s= +e_1,r=e_3)} (\pm c)$$
$$\large \rho^{- x}_{l,r}(\lambda,\alpha) = \underline{M(\lambda + 1,\alpha,s=-e_1,r=e_3)} (\pm c)$$
$$\large \rho^{+ y}_{l,r}(\lambda,\alpha) = \underline{M(\lambda + \frac{3}{2} ,\alpha,s=+e_2,r=e_3)} (\pm c) $$
$$\large \rho^{- y}_{l,r}(\lambda,\alpha) = \underline{M(\lambda + \frac{1}{2} ,\alpha,s=-e_2,r=e_3)} (\pm c) $$
$$\large \rho^{+ z}_{l,r}(\lambda,\alpha) = \underline{R_{12}(\frac{\lambda}{2})M(\frac{1}{2},\alpha,s=+ e_3,r=e_2))} (\pm c) $$
$$\large \rho^{- z}_{l,r}(\lambda,\alpha) = \underline{R_{12}(\frac{\lambda}{2})M(\frac{3}{2},\alpha,s=- e_3,r=e_2))} (\pm R_{12}(\frac{-\lambda}{2}) c R_{12}(\frac{-\lambda}{2})^\dagger).$$
Where we used $\underbar{M}(x)$ to denote the sandwich-product $MxM^\dagger$ of $x$.

References:

[1] Belon, M.C.L., Hildenbrand, D. Practical Geometric Modeling Using Geometric Algebra Motors. Adv. Appl. Clifford Algebras 27, 2019–2033 (2017). https://doi.org/10.1007/s00006-017-0777-z
