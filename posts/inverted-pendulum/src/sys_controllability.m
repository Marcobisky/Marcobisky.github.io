clear all; close all; clc;

% Simulation parameters
m = 3;          % Mass of pendulum
M = 5;         % Mass of cart
L = 1;          % Length of pendulum
g = -9.81;       % Gravity
b = 5;          % damping coefficient

% Define matrix, xdot = Ax + Bu
A = [0, 1,          0,              0;
     0, -b/M,       -m*g/M,         0;
     0, 0,          0,              1;
     0, -b/(M*L),   -(M+m)*g/(M*L), 0];

B = [0; 1/M; 0; -1/(M*L)];

rank(ctrb(A, B))