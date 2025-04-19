---
author: Marcobisky
title: Test
description: None
date: 2025-4-5
# image: cover.png
categories:
    - Algebra
format: 
    html: default
---

## Takeaways

## Projective Space


2. Rotation in $\mathbb{C}^2$ sits bijectively on the surface of the 3-sphere $S^3$:
$$
SU(2) \simeq \mathbb{S}^3
$$

<!-- ----------------------------------------- -->
::: {.callout-tip icon=false}
## Proof
An element in $SU(2)$ has the form:
$$
U = \begin{pmatrix} \alpha & \gamma \\ \beta & \delta \\\end{pmatrix} \in SU(2)
$$
with constraints:
$$
U^H = U^{-1}, \det U = 1.
$$
Therefore,
$$
\begin{pmatrix} \bar{\alpha} & \bar{\beta} \\ \bar{\gamma} & \bar{\delta} \\\end{pmatrix}
=
\frac{1}{\det U} \begin{pmatrix} \delta & -\gamma \\ -\beta & \alpha \\\end{pmatrix}
=
\begin{pmatrix} \delta & -\gamma \\ -\beta & \alpha \\\end{pmatrix}.
$$
Thus, $U$ must look like:
$$
\begin{align*}
& U = \begin{pmatrix} \alpha & -\beta \\ \beta & \bar{\alpha} \\\end{pmatrix}, \text{ with } \det U = 1 \\
\implies\quad & \alpha \bar{\alpha} + \beta \bar{\beta} = 1 \\
\implies\quad & |\alpha|^2 + |\beta|^2 = 1 \\
\implies\quad & |a + bi|^2 + |c + di|^2 = 1 \\
\implies\quad & a^2 + b^2 + c^2 + d^2 = 1.
\end{align*}
$$
So,
$$
\forall U \in SU(2), U \in \mathbb{S}^3.
$$
:::
<!-- ----------------------------------------- -->