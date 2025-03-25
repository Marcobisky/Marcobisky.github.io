function invpend_plot(x, L, saveGif, gifFileName)
    % Extract state variables
    cart_x = x(1);    % Cart position
    theta = x(3);     % Pendulum angle
    
    % Compute pendulum position
    pend_x = cart_x + L * sin(theta);
    pend_y = L * cos(theta);
    
    % Figure setup
    clf; hold on; axis equal; grid on;
    xlim([-2 2]); ylim([-1.5 1.5]);
    
    % Draw cart
    cart_w = 0.4; cart_h = 0.2;
    rectangle('Position', [cart_x - cart_w/2, -cart_h/2, cart_w, cart_h], ...
              'Curvature', 0.1, 'FaceColor', [0.5 0.5 0.5]);
    
    % Draw pendulum
    plot([cart_x, pend_x], [0, pend_y], 'k-', 'LineWidth', 2); % Rod
    plot(pend_x, pend_y, 'ro', 'MarkerSize', 10, 'MarkerFaceColor', 'r'); % Mass
    
    % Draw ground
    plot([-2 2], [0, 0], 'k', 'LineWidth', 2);
    
    % If saveGif is true, save the current frame to a GIF file
    persistent gifFile frameCount currentGifName
    if nargin < 3
        saveGif = false;
    end
    
    if saveGif
        % Set default filename if not provided
        if nargin < 4 || isempty(gifFileName)
            gifFileName = 'invpend_animation.gif';
        end
        
        % Reset frame count if this is a new gif file
        if isempty(currentGifName) || ~strcmp(currentGifName, gifFileName)
            frameCount = 1;
            currentGifName = gifFileName;
        else
            frameCount = frameCount + 1;
        end
        
        % Capture the current figure as an image
        frame = getframe(gcf);
        im = frame2im(frame);
        [imind, cm] = rgb2ind(im, 256);
        
        % Write to the GIF file
        if frameCount == 1
            imwrite(imind, cm, gifFileName, 'gif', 'Loopcount', inf, 'DelayTime', 0.1);
        else
            imwrite(imind, cm, gifFileName, 'gif', 'WriteMode', 'append', 'DelayTime', 0.1);
        end
    end
    
    drawnow;
end