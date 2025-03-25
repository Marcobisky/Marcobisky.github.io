clear all; close all; clc;

%% Simulation parameters
m = 2;          % Mass of pendulum
M = 10;         % Mass of cart
L = 1;          % Length of pendulum
g = -9.81;       % Gravity
b = 2;          % damping coefficient
time = 0:.4:100; % Time samples

%% Initial conditions
x0 = [0; 0; -.4; 0]; % x, xdot, theta, thetadot

%% LQR pole placement

% Define matrix, xdot = Ax + Bu
A = [0, 1,          0,              0;
     0, -b/M,       -m*g/M,         0;
     0, 0,          0,              1;
     0, -b/(M*L),   -(M+m)*g/(M*L), 0];

B = [0; 1/M; 0; -1/(M*L)];

% Define penalty Q and R matrix
% Desired: Move the cart to the desired position as fast as possible
% Q = [400, 0,  0,  0;
%      0, 50,  0,  0;
%      0, 0,  1,  0;
%      0, 0,  0,  1];

% Desired: Move the cart as smooth as possible
Q = [20, 0,  0,  0;
     0, 400,  0,  0;
     0, 0,  1,  0;
     0, 0,  0,  1];

% Desired: Don't change the angle so much
% Q = [4, 0,  0,  0;
%      0, 4,  0,  0;
%      0, 0,  500,  0;
%      0, 0,  0,  50];

% Desired: Save energy
R = .01;

K = lqr(A, B, Q, R)

% Just to verify the stability of the closed loop system
eig(A - B*K)

%% Solve ODE
desired_state_vec = [1; 0; 0; 0];
[t, x] = ode45(@(t, x) invpend(x, m, M, L, g, b, -K * (x - desired_state_vec)), time, x0);

%% Animation
for k = 1:length(t)
    invpend_plot(x(k, :), L, true, 'simulation_lqr_4.gif');
    % invpend_plot(x(k, :), L, false);
end
