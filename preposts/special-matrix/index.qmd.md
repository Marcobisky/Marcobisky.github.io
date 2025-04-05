---
author: Marcobisky
title: Special Matrices
description: test
date: 2025-3-15
# image: cover.png
categories:
    - Algebra
format: 
    html: default
    pdf: default
citation-location: margin
---

## Big Picture

## Normal Operator

<!-- ----------------------------------------- -->
::: {.callout-tip icon=false}
## Definition: Normal Operator
::: {#def-normal-operator .callout-def}
$A \in \mathbb{C}^{n \times n}$ is called ***normal*** iff $A^H A = AA^H$
:::
:::
<!-- ----------------------------------------- -->

### Notes

1. $\iff$ $A$ is *unitarily-diagonalizable*, i.e.,
    $$
    \exists U \in U(n), \text{diagonal } D, \text{s.t. } A = UDU^H. \quad (\text{Spectral Thm 2})
    $$

    $\iff$ $\exists \text{ orthogonal eigenvectors that span } \mathbb{C}^n.$

    $\iff$ $A \text{ orthogonally non-defective}$

    $\iff$ $\text{row covariance matrix of }A = \text{column covariance matrix of }A$

2. Normal matrix $A$ does not necessarily invertible. Its eigenvalues can be $0, \mathbb{R}$ or $\mathbb{C}$.

3. Mental picture for normal operator:

    $$
    \boxed{\text{Normal operators} \iff \text{Squeezing complex rectangular box.}}
    $$

## Hermitian (Self-adjoint) Operator

<!-- ----------------------------------------- -->
::: {.callout-tip icon=false}
## Definition: Hermitian Operator
::: {#def-hermitian-operator .callout-def}
$A \in \mathbb{C}^{n \times n}$ is called ***hermitian (self-adjoint)*** iff $A = A^H$
:::
:::
<!-- ----------------------------------------- -->

### Notes

1. 
$$
A \text{ hermitian}
\iff \begin{equation*}
  \begin{cases} A \text{ normal} &  \\ \text{spectrum of }A \subseteq \mathbb{R}. &  \end{cases}
\end{equation*}
$$

2. Also self-adjoint operators do not necessarily invertible.

3. Self-adjoint operators could be think of as normal operators with real spectrum.

4. Mental picture for hermitian operators:

    $$
    \boxed{\text{Hermitian operators} \iff \text{Squeezing complex rectangular box in a particular way that creatures living under projection }\pi: \mathbb{C}^n \to \mathbb{R}^n \text{ do NOT think it is a rotation.}}
    $$

5. If $A \in \mathbb{R}^{n\times n} < \mathbb{C}^{n\times n}$ is hermitian, it is also called ***symmetric***, i.e.,
    $$
    A = A^t.
    $$


## Skew-Hermitian Operator

<!-- ----------------------------------------- -->
::: {.callout-tip icon=false}
## Definition: Hermitian Operator
::: {#def-skew-hermitian-operator .callout-def}
$A \in \mathbb{C}^{n \times n}$ is called ***skew-hermitian*** iff $-A = A^H$
:::
:::
<!-- ----------------------------------------- -->

### Notes

1. Skew-hermitian operators are very close to hermitian:
    $$
    A \text{ skew-hermitian} \iff iA \text{ hermitian}
    $$

<!-- ----------------------------------------- -->
::: {.callout-note icon=true collapse=true}
## Proof
Let $A \in \mathbb{C}^{n \times n}$ be skew-hermitian, i.e., $-A = A^H$. Let $B = iA$. Then
$$
B^H = (iA)^H = -iA^H = iA = B.
$$

Therefore, $B$ is hermitian.
:::
<!-- ----------------------------------------- -->


2. By the property that hermitian operators have real spectrum, **all skew-hermitian operators have purely imaginary spectrum.**

3.
$$
A \text{ skew-hermitian}
\iff \begin{equation*}
  \begin{cases} A \text{ normal} &  \\ \text{spectrum of }A \subseteq i\mathbb{R}. &  \end{cases}
\end{equation*}
$$

## Unitary Operator

<!-- ----------------------------------------- -->
::: {.callout-tip icon=false}
## Definition: Unitary Operator
::: {#def-unitary-operator .callout-def}
$A \in \mathbb{C}^{n \times n}$ is called ***unitary*** iff $AA^H = I$, denoted $A \in U(n)$
:::
:::
<!-- ----------------------------------------- -->

<!-- ----------------------------------------- -->
::: {.callout-tip icon=false}
## Proposition
::: {#prp- .callout-prp}
$$
\begin{equation*}
    \begin{cases} A \text{ square} &  \\ A^HA = I &  \end{cases}

    \implies A A^H = I
\end{equation*}
$$
:::
:::
<!-- ----------------------------------------- -->

::: {.proof}
From $A^H A = I$ we know that the *columns* of $A$ are *orthonormal*

$\implies$ $A$ injective

Also $A$ is square. Since injective automorphisms are epimorphisms, we have:

$\implies$ $A$ is an isomorphism

$\implies$ $A$ is invertible, and $A^H = A^{-1}$

This finished the proof.
:::

### Notes

1. Hence for unitary operators:
    $$
    A^H A = A A^H = I
    $$

2.
$$
\begin{aligned}
    & \iff \begin{equation*}
  \begin{cases} A \text{ normal} &  \\ \text{spectrum of }A \subseteq \mathbb{S}^1 \subseteq \mathbb{C} &  \end{cases}
\end{equation*} \\

& \iff A^H = A^{-1} \\

& \iff \begin{equation*}
  \begin{cases} A \text{ square} &  \\ A^H A = I  &  \end{cases}
\end{equation*} \\

& \iff \begin{equation*}
  \begin{cases} A \text{ square} &  \\ A A^H = I.  &  \end{cases}
\end{equation*} \\

\end{aligned}
$$


## Rotation Matrix (Special Unitary)