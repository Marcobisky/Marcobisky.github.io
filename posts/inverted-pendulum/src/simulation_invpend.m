clear all; close all; clc;

% Simulation parameters
m = 2;          % Mass of pendulum
M = 4;         % Mass of cart
L = 1;          % Length of pendulum
g = -9.81;       % Gravity
b = 30;          % damping coefficient
time = 0:.1:10; % Time samples

% Initial conditions
x0 = [0; 0; .2; 0]; % x, xdot, theta, thetadot

% Solve ODE
[t, x] = ode45(@(t, x) invpend(x, m, M, L, g, b, 0), time, x0);

% Animation
for k = 1:length(t)
    invpend_plot(x(k, :), L, true, 'simulation_invpend.gif');
end
