% x -> state vector (x, xdot, theta, thetadot)
% m -> mass of pendulum
% M -> mass of cart
% L -> length of pendulum
% g -> gravity
% b -> friction = -b*xdot
% F -> force applied to cart
% dx -> derivative of state vector

function dx = invpend(x, m, M, L, g, b, F)
    % Unpack state variables
    x1 = x(1);     % cart position
    x2 = x(2);     % cart velocity (xdot)
    x3 = x(3);     % pendulum angle (theta)
    x4 = x(4);     % angular velocity (thetadot)
    
    % Precompute useful terms
    sin_theta = sin(x3);
    cos_theta = cos(x3);
    theta_dot = x4;
    
    % Mass matrix
    D = [M + m,         m * L * cos_theta;
         m * L * cos_theta,   m * L^2];

    % Right-hand side (forces/accelerations)
    RHS = [F - b * x2 + m * L * sin_theta * theta_dot^2;
           -m * g * L * sin_theta];

    % Solve for accelerations
    accel = D \ RHS;  % Equivalent to inv(D) * RHS, but more stable
    
    % Return time derivative of state vector
    dx = zeros(4, 1);
    dx(1) = x2;         % xdot
    dx(2) = accel(1);   % xddot
    dx(3) = x4;         % thetadot
    dx(4) = accel(2);   % thetaddot
end