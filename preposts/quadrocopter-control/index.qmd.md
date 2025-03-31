---
author: Marcobisky
title: Quadrocopter Control
description: test
date: 2025-3-25
# image: cover.png
categories:
    - Control-Theory
format: 
    html:
        toc: true
        self-contained: true
        grid: 
            margin-width: 350px
    pdf: default
html-math-method: mathjax
reference-location: margin
citation-location: margin
---

## Model

### Dynamics Equations without thrust


The dynamics $\dot{\mathbf{x}} = \phi(\mathbf{x})
$ is given by:


Position dynamics:

 $$\dot{\mathbf{r}} = \mathbf{v}$$

Velocity dynamics (Newton's second law with only gravity):

 $$\dot{\mathbf{v}} = -g\mathbf{e}_3$$

Orientation dynamics (quaternion kinematics):

 $$\dot{q} = \frac{1}{2}q \cdot p(\boldsymbol{\Omega})$$


As shown in equation (20) of the paper:

 $$\dot{q} = \begin{pmatrix} \dot{q}_0 \\ \dot{q}_{1:3} \end{pmatrix} = \frac{1}{2} \begin{pmatrix} -q_{1:3}^T\boldsymbol{\Omega} \\ (S(q_{1:3}) + q_0\mathbf{I})\boldsymbol{\Omega} \end{pmatrix}$$

Where $S(q1:3)S(q_{1:3})
S(q1:3​)$ is the skew-symmetric matrix:

 $$S(q_{1:3}) = \begin{pmatrix} 0 & -q_3 & q_2 \\ q_3 & 0 & -q_1 \\ -q_2 & q_1 & 0 \end{pmatrix}$$

Angular velocity dynamics (Euler's equations without external torques):

 $$\dot{\boldsymbol{\Omega}} = -\mathbf{J}^{-1}(\boldsymbol{\Omega} \times (\mathbf{J}\boldsymbol{\Omega}))$$

$$\dot{\mathbf{x}} = \phi(\mathbf{x}) = \begin{pmatrix}
\mathbf{v} \
-g\mathbf{e}_3 \
\frac{1}{2}q \cdot p(\boldsymbol{\Omega}) \
-\mathbf{J}^{-1}(\boldsymbol{\Omega} \times (\mathbf{J}\boldsymbol{\Omega}))
\end{pmatrix}$$


It's worth noting that this represents the dynamics of a free-falling quadrocopter with no thrust forces (as the human specified "without control"). In reality, even in a passive state, a quadrocopter would have some baseline thrust from spinning propellers.
For a more realistic "passive" model, we could include a constant collective thrust ff
f acting along the body's z-axis, which would modify the velocity dynamics to:

$$
\dot{\mathbf{v}} = -g \mathbf{e}_3 + \frac{f}{m} R(q) \mathbf{e}_3
$$

Where $R(q)$ is the rotation matrix corresponding to quaternion $q$.

These equations capture the full nonlinear dynamics of the quadrocopter in phase space, representing how position, velocity, orientation, and angular velocity evolve over time in the absence of control inputs.


### Dynamics Equations with thrust

# Quadrocopter Dynamics with Motor Control in Phase Space

## State Vector and Basic Parameters

As before, the state vector in phase space is:
$$\mathbf{x} = (\mathbf{r}, \mathbf{v}, q, \boldsymbol{\Omega})$$

Where:
- $\mathbf{r} \in \mathbb{R}^3$ is the position in inertial frame
- $\mathbf{v} \in \mathbb{R}^3$ is the linear velocity in inertial frame
- $q \in \mathbb{S}^3$ is the unit quaternion representing orientation
- $\boldsymbol{\Omega} \in \mathbb{R}^3$ is the angular velocity vector in body frame

## Motor and Physical Parameters

- $m$: mass of the quadrocopter
- $\mathbf{J} \in \mathbb{R}^{3 \times 3}$: inertia tensor (typically diagonal for a symmetric quadrocopter)
- $g$: gravitational acceleration (9.81 m/s²)
- $L$: distance from center of mass to each motor (arm length)
- $k_T$: thrust coefficient (converts squared motor speed to thrust force)
- $k_M$: moment coefficient (relates thrust to reactive torque)
- $\omega_i$: angular velocity of motor $i$ for $i \in \{1,2,3,4\}$
- $\mathbf{e}_3 = (0,0,1)^T$: unit vector in the z-direction

## Motor Forces and Torques

Each motor produces:
- Thrust force: $F_i = k_T\omega_i^2$
- Reactive torque: $M_i = k_M\omega_i^2$

For a typical "+" configuration (1-front, 2-right, 3-back, 4-left):

1. Total thrust: $F = \sum_{i=1}^4 F_i = k_T\sum_{i=1}^4 \omega_i^2$

2. Moment vector in body frame:
   $$\boldsymbol{\tau} = \begin{pmatrix} \tau_x \\ \tau_y \\ \tau_z \end{pmatrix} = \begin{pmatrix} 
   L(F_4 - F_2) \\
   L(F_1 - F_3) \\
   M_1 - M_2 + M_3 - M_4
   \end{pmatrix}$$

   Substituting motor forces:
   $$\boldsymbol{\tau} = \begin{pmatrix} 
   Lk_T(\omega_4^2 - \omega_2^2) \\
   Lk_T(\omega_1^2 - \omega_3^2) \\
   k_M(\omega_1^2 - \omega_2^2 + \omega_3^2 - \omega_4^2)
   \end{pmatrix}$$

## Control Input Mapping

We can define a mapping from motor speeds to control inputs:
$$\begin{pmatrix} F \\ \tau_x \\ \tau_y \\ \tau_z \end{pmatrix} = 
\begin{pmatrix} 
k_T & k_T & k_T & k_T \\
0 & -Lk_T & 0 & Lk_T \\
Lk_T & 0 & -Lk_T & 0 \\
k_M & -k_M & k_M & -k_M
\end{pmatrix}
\begin{pmatrix} \omega_1^2 \\ \omega_2^2 \\ \omega_3^2 \\ \omega_4^2 \end{pmatrix}$$

## Dynamics Equations with Control

1. **Position dynamics**: 
   $$\dot{\mathbf{r}} = \mathbf{v}$$

2. **Velocity dynamics** (with thrust force):
   $$\dot{\mathbf{v}} = -g\mathbf{e}_3 + \frac{F}{m}R(q)\mathbf{e}_3$$
   
   Where $R(q)$ is the rotation matrix corresponding to quaternion $q$, which transforms the body-fixed thrust direction to the inertial frame.

3. **Orientation dynamics** (quaternion kinematics):
   $$\dot{q} = \frac{1}{2}q \cdot p(\boldsymbol{\Omega})$$
   
   As expressed in component form:
   $$\dot{q} = \begin{pmatrix} \dot{q}_0 \\ \dot{q}_{1:3} \end{pmatrix} = \frac{1}{2} \begin{pmatrix} -q_{1:3}^T\boldsymbol{\Omega} \\ (S(q_{1:3}) + q_0\mathbf{I})\boldsymbol{\Omega} \end{pmatrix}$$
   
   Where $S(q_{1:3})$ is the skew-symmetric matrix of the vector part of the quaternion.

4. **Angular velocity dynamics** (Euler's equations with motor torques):
   $$\dot{\boldsymbol{\Omega}} = \mathbf{J}^{-1}(\boldsymbol{\tau} - \boldsymbol{\Omega} \times (\mathbf{J}\boldsymbol{\Omega}))$$

## Complete System Dynamics

The full dynamics of the controlled quadrocopter in phase space are:

$$\dot{\mathbf{x}} = \phi(\mathbf{x}, \mathbf{u}) = \begin{pmatrix} 
\mathbf{v} \\
-g\mathbf{e}_3 + \frac{F}{m}R(q)\mathbf{e}_3 \\
\frac{1}{2}q \cdot p(\boldsymbol{\Omega}) \\
\mathbf{J}^{-1}(\boldsymbol{\tau} - \boldsymbol{\Omega} \times (\mathbf{J}\boldsymbol{\Omega}))
\end{pmatrix}$$

Where the control input $\mathbf{u} = (\omega_1^2, \omega_2^2, \omega_3^2, \omega_4^2)$ represents the squared motor speeds.

These nonlinear differential equations fully describe the quadrocopter's motion under motor control, capturing the complex interactions between thrust forces, aerodynamic torques, and rigid body dynamics.

Note that in practice, there may be additional terms for aerodynamic drag, motor dynamics, and other effects, but this model captures the essential physics of quadrocopter flight with motor control.