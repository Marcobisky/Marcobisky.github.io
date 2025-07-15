---
author: Marcobisky
title: Spinors Notes
draft: true
description: "[fill in the cross citations]"
date: 2025-4-22
# image: cover.png
categories:
    - Differential-Geometry
    - EN-blogs
format: 
    html: default
bibliography: refs.bib
bibliographystyle: ieee
csl: diabetologia.csl #https://github.com/citation-style-language/styles
---

### Pauli vectors

We already know in [this post](../projective-space/index.qmd) that:
$$
\boxed{
\text{Spin}(3) \simeq SU(2) \simeq \mathbb{S}^3 \simeq U(\mathbb{H}) \overset{2:1} \twoheadrightarrow \mathbb{RP}^3 \simeq SO(3).
}
$${#eq-main-relation}

I'm most familiar with $SO(3)$ in @eq-main-relation since they just left-operate on vectors in $\mathbb{R}^3$:
$$
\begin{bmatrix} a \\ b \\ c \\\end{bmatrix}
\mapsto
\overbrace{
\begin{bmatrix} | & | & | \\ e_1' & e_2' & e_3' \\ | & | & | \\\end{bmatrix}}^{\in SO(3)}
\begin{bmatrix} a \\ b \\ c \\\end{bmatrix}.
$$

But @eq-main-relation tells us that elements in $SU(2), U(\mathbb{H})$ could also be used to represent rotations in $\mathbb{R}^3$ in the sense that two opposite elements in them represent the same rotation. But how *exactly* do they represent? You can't just multiply a $2 \times 2$ complex matrix or a unit quaternion with a $3 \times 1$ column vector to rotate it. It turns out that we need to use alternative representations of the vectors in $\mathbb{R}^3$, in terms of matrices and quaternions in the following way:
$$
\overbrace{\begin{bmatrix} a \\ b \\ c \\\end{bmatrix}}^{\in \mathbb{R}^3}
\leftrightsquigarrow
\overbrace{\begin{pmatrix} c & a-bi \\ a+bi & -c \\\end{pmatrix}}^{\in SU(2)}
\leftrightsquigarrow
\overbrace{a \mathbf{i} + b \mathbf{j} + c \mathbf{k}}^{\in \Im(\mathbb{H})}.
$$

Also a different representation of the rotation matrices in $SO(3)$:
$$
\overbrace{
\begin{bmatrix} | & | & | \\ e_1' & e_2' & e_3' \\ | & | & | \\\end{bmatrix}}^{\in SO(3)}
\begin{bmatrix} \\ \cdot \\ \\\end{bmatrix}
\leftrightsquigarrow
\overbrace{\begin{pmatrix} \Box & \Box \\ \Box & \Box \\\end{pmatrix}}^{\in SU(2)}

$$

### Pauli vectors are in $\text{Herm}_0(2, \mathbb{C})$

<!-- ----------------------------------------- -->
::: {.callout-tip icon=false}
## Pauli Vectors
::: {#def-pauli-vectors .callout-def}
**Pauli vectors** are *traceless hermitian* $2 \times 2$ complex matrices. Hence, they must take the form:
$$
\begin{pmatrix} c & a-bi \\ a+bi & -c \\\end{pmatrix}, \quad \forall a,b,c \in \mathbb{R}.
$${#eq-pauli-vectors-form}
:::
:::
<!-- ----------------------------------------- -->

The set of all Pauli vectors is denoted by $\text{Herm}_0(2, \mathbb{C})$. What’s unexpected is just how faithfully these matrices replicate the behavior of vectors in $\mathbb{R}^3$:

> As [**lie algebras**](https://en.wikipedia.org/wiki/Lie_algebra), $$\text{Herm}_0(2, \mathbb{C}) \simeq \mathbb{R}^3.$$

The correspondence is given in the 

|| $\mathbb{R}^3$ | $\text{Herm}_0(2, \mathbb{C})$| $\mathfrak{su}(2)$ | $\Im(\mathbb{H})$ | $\mathfrak{so}(3)$ |
|----------------------|----------------------------------------------|-------------------------------------------------|----------------------|-------------------|-------------------|
| **Decomposition** | $v = v^ie_i$ | $H_v = v^i \sigma_i$ | | $q_v = v^1 \mathbf{i} + v^2 \mathbf{j} + v^3 \mathbf{k}$ |
| **Basis vectors** | $\{e_i\}=\left\{ \begin{bmatrix} 1 \\ 0 \\ 0 \end{bmatrix}, \begin{bmatrix} 0 \\ 1 \\ 0 \end{bmatrix}, \begin{bmatrix} 0 \\ 0 \\ 1 \end{bmatrix} \right\}$ | $\{\sigma_i\}=\left\{\begin{pmatrix} 0 & 1 \\ 1 & 0 \\\end{pmatrix},\begin{pmatrix} 0 & -i \\ i & 0 \\\end{pmatrix},\begin{pmatrix} 1 & 0 \\ 0 & -1 \\\end{pmatrix} \right\} \\ \text{(Pauli matrices)}$ | $\{u_i\}=\left\{\begin{pmatrix} 0 & i \\ i & 0 \\\end{pmatrix},\begin{pmatrix} 0 & -1 \\ 1 & 0 \\\end{pmatrix},\begin{pmatrix} i & 0 \\ 0 & -i \\\end{pmatrix} \right\}$ | $\{\mathbf{i}, \mathbf{j}, \mathbf{k}\}$ |
| **Norm** | $\lVert v \rVert = \sqrt{v_1^2 + v_2^2 + v_3^2}$ | $\lVert H_v \rVert = \sqrt{ \frac{1}{2} \mathrm{Tr}(H_v^2) }$ | | $\lVert q \rVert = q\bar{q}$ |
| **Inner product** | $\langle \vec{v}, \vec{w} \rangle = v^iw^i$ | $\langle H_v, H_w \rangle = \frac{1}{2} \mathrm{Tr}(H_vH_w)$ | | $\langle q_v, q_w \rangle = -\Re(q_vq_w)$ |
| **Lie bracket** | $\vec{v} \times \vec{w}$ | $[H_v, H_w] := -i(H_vH_w - H_wH_v)$ | | $\Im(q_vq_w)$ |
| **Lie bracket on basis** | $e_i \times e_j = \epsilon_{ijk} e_k$ | $[\sigma_i, \sigma_j] = 2i\epsilon_{ijk} \sigma_k$ | | $\mathbf{i} \times \mathbf{j} = \mathbf{k}$ |
| **Rotation** | $v \mapsto \underbrace{\begin{bmatrix} && \\ & SO(3) &\\&& \\\end{bmatrix}}_{\mathclap{\text{\scriptsize columns: new basis coor.}}} v$ | $H_v \mapsto \underbrace{\biggl(SU(2)\biggl)}_{\mathclap{\scriptsize \pm \left(\cos \frac{\theta}{2} I+i\sin \frac{\theta}{2} (H_{\text{axis}})\right)}} H_v \biggl(SU(2)\biggl)^\dagger$ | | $q_v \mapsto \underbrace{u}_{\mathclap{\scriptsize \pm \left(\cos \frac{\theta}{2} + \sin \frac{\theta}{2} (q_{\text{axis}}) \right)}} q_v \bar{u}, u \in U(\mathbb{H})$ |



### Bilinear space and isometry

> A **bilinear space** is nearly an **inner product space** without the (conjugate) symmetric and positive-definite properties. It's a compromise when inner products are hard to define[^similar-ideas]. 

[^similar-ideas]: Just like we come up with *pseudo-riemannian* manifolds when the requirement of positive-definiteness is relaxed.

<!-- ----------------------------------------- -->
::: {.callout-tip icon=false}
## Bilinear space @szechtman_2005_structure
::: {#def-bilinear-space .callout-def}
Let $V$ be a vector space over field $\mathbb{F}$ and $B: V \times V \to \mathbb{F}$ a bilinear form[^bilinear-form-notation]. A **bilinear space** is the pair $(V, B)$.
:::
:::
<!-- ----------------------------------------- -->

[^bilinear-form-notation]: Sometimes $B$ is denoted using the inner product notation $\langle \cdot , \cdot \rangle$. But it's NOT inner product!

> The bijective linear transformation between two bilinear spaces that preserves the bilinear form is called an **isometry**[^isometry].

[^isometry]: Isometry also refers to the distance-preserving map between two metric spaces. 

<!-- ----------------------------------------- -->
::: {.callout-tip icon=false}
## Isometry between bilinear spaces @szechtman_2005_structure
::: {#def-isometry .callout-def}
An isometry from a bilinear space $(V_1,B_1)$ to a bilinear space $(V_2,B_2)$ is a linear
isomorphism $L : V_1 \to V_2$ satisfying:
$$
B_2(Lx, Ly) = B_1(x,y), \quad \forall x,y \in V_1.
$$
:::
:::
<!-- ----------------------------------------- -->

> All isometries from a bilinear space $(V,B)$ to itself form a group called the **isometry group** $G(V, B)$.