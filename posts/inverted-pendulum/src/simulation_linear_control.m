clear all; close all; clc;

%% Simulation parameters
m = 2;          % Mass of pendulum
M = 10;         % Mass of cart
L = 1;          % Length of pendulum
g = -9.81;       % Gravity
b = 2;          % damping coefficient
time = 0:.1:6; % Time samples

%% Initial conditions
x0 = [0; 0; -.4; 0]; % x, xdot, theta, thetadot

%% pole placement

% Define matrix, xdot = Ax + Bu
A = [0, 1,          0,              0;
     0, -b/M,       -m*g/M,         0;
     0, 0,          0,              1;
     0, -b/(M*L),   -(M+m)*g/(M*L), 0];

B = [0; 1/M; 0; -1/(M*L)];

desired_eigs_vec = [-3; -4; -5; -6];
K = place(A, B, desired_eigs_vec);

% Just to verify that the poles are where we want them
eig(A - B*K)

%% Solve ODE
desired_state_vec = [1; 0; 0; 0];
[t, x] = ode45(@(t, x) invpend(x, m, M, L, g, b, -K * (x - desired_state_vec)), time, x0);

%% Animation
for k = 1:length(t)
    invpend_plot(x(k, :), L, true, 'simulation_linear_control.gif');
end
