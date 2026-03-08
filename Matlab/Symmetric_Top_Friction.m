function Symmetric_Top_Friction()
    clc
    close all
    clear all
    
    %% Dynamic Parameters
    M = 1; % Mass of M
    R = 0.5; %Radius of M
    g =[0 0 -9.81]; % Acceleration due to gravity
    L = 1.5; %Length of CM to O
    I = 1/2*M*R^2;
    omega = 50;
    theta = pi/6;
    k = 0.1;

    %% Initial Data
    dt = 0.001; % Time resolution

    % Pendulum
    r0 = L*[sin(theta) 0 cos(theta)];
    N_orbit0 = 400;

    % Center
    r1 = [0 0 0];


    %% Process
    t = 0;
    orbit_array0 = zeros(3,N_orbit0);
    orbit_array0(:,end) = r0;
    orbit_array1 = zeros(3,N_orbit0);
    orbit_array1(:,end) = r1;
    orbit_array2 = zeros(3,N_orbit0);
    orbit_array2(:,end) = 2*r0;

    %% FIGURE
    figure('name','Physics','color','white','numbertitle','off','units','normalized','outerposition',[0 0 1 1]);
    set(gca,'color','white','xcolor','black','ycolor','black','zcolor','black');
    hold on
    % Plot Orbit
    hf0 = plot3(orbit_array0(1,end),orbit_array0(2,end),orbit_array0(3,end),'ro','markersize',2,'markerfacecolor','r');
    hf_orbit0 = plot3(orbit_array0(1,:),orbit_array0(2,:),orbit_array0(3,:),'ko','markersize',1);
    hf1 = plot3(orbit_array1(1,end),orbit_array1(2,end),orbit_array1(3,end));
    hf2 = plot3(orbit_array2(1,end),orbit_array2(2,end),orbit_array2(3,end));
    hf_orbit2 = plot3(orbit_array2(1,:),orbit_array2(2,:),orbit_array2(3,:),'ko','markersize',1);
    % Draw dashed line
    hstick = plot3([orbit_array0(1,end) orbit_array1(1,end)], [orbit_array0(2,end) orbit_array1(2,end)], [orbit_array0(3,end) orbit_array1(3,end)], '-', 'Color', 'r','LineWidth',4);
    hvec = plot3([orbit_array0(1,end) orbit_array2(1,end)], [orbit_array0(2,end) orbit_array2(2,end)], [orbit_array0(3,end) orbit_array2(3,end)], '--', 'Color', 'k','LineWidth',2);
    hdashed2 = quiver3(orbit_array0(1,end), orbit_array0(2,end), orbit_array0(3,end), ...
                   orbit_array2(1,end)-orbit_array0(1,end), ...
                   orbit_array2(2,end)-orbit_array0(2,end), ...
                   orbit_array2(3,end)-orbit_array0(3,end), 0,'Color', 'k', 'LineWidth', 2);

    ht1 = title(sprintf('t = %0.2f s',t),'color','black');

    % Line
    lx = line([-3 3],[0 0],[0 0], 'Color','black', 'LineWidth',1,'LineStyle','-');
    lxtext = text(3.1,0,0,'$x$');
    ly = line([0 0],[-3 3],[0 0], 'Color','black', 'LineWidth',1,'LineStyle','-');
    lytext = text(0,3.1,0,'$y$');
    lz = line([0 0],[0 0],[0 3], 'Color','black', 'LineWidth',1,'LineStyle','-');
    lztext = text(0,0,3.1,'$z$');

    % Circle
    center = 0.75*[orbit_array0(1,end) orbit_array0(2,end) orbit_array0(3,end)];
    radius = R;
    theta0 = 0:0.01:2*pi;
    v = null(orbit_array0(:,end)');
    points = repmat(center',1,size(theta0,2))+radius*(v(:,1)*cos(theta0)+v(:,2)*sin(theta0));
    hcirclefill = fill3(points(1,:),points(2,:),points(3,:),'b','FaceAlpha',0.5); % Fill the circle with red color
    hcircleline = plot3(points(1,:),points(2,:),points(3,:),'r-','LineWidth',2);

    center1 = [0 0 2*L*cos(theta)];
    theta1=0:0.01:2*pi;
    radius1 = 2*L*sin(theta);
    v1 = null([0 0 1]);
    points1=repmat(center1',1,size(theta1,2))+radius1*(v1(:,1)*cos(theta1)+v1(:,2)*sin(theta1));
    plot3(points1(1,:),points1(2,:),points1(3,:),'k--','LineWidth',1);

    axis equal
    axis([-4 4 -4 4 0 4]);
    title('Simulation','FontSize',20);
    view(3);
    rotate3d on
    xlabel('$x$ (m)','fontsize',30,'color','black','Interpreter', 'latex');
    ylabel('$y$ (m)','fontsize',30,'color','black','Interpreter', 'latex');
    zlabel('$z$ (m)','fontsize',30,'color','black','Interpreter', 'latex');
    grid on

    %% CALCULATION
    z = 20; % Real time in seconds
    % Create a VideoWriter object
    vid = VideoWriter('SymmetricTop.mp4', 'MPEG-4');
    open(vid);
    for ts = 0:z/dt
       t = ts.*dt;

       % Equations of motion
         r_xy = norm(r0(1:2));
         if r_xy > eps
           e = -(1/r_xy)*[r0(1) r0(2) 0];
         else
           e = [0 0 0];
         end
       v0 = (M*cross(r0,g) + k*M*norm(g)*e)*norm(r0)./(I.*omega);
       r0 = r0 + v0.*dt;

       % Orbit tracer
       orbit_array0(:,1:end-1) = orbit_array0(:,2:end);
       orbit_array0(:,end) = r0;
       orbit_array1(:,1:end-1) = orbit_array1(:,2:end);
       orbit_array1(:,end) = r1;
       orbit_array2(:,1:end-1) = orbit_array2(:,2:end);
       orbit_array2(:,end) = 2*r0;
       % Update plot
       set(hf0,'xdata',orbit_array0(1,end),'ydata',orbit_array0(2,end),'zdata',orbit_array0(3,end));
       set(hf_orbit0,'xdata',orbit_array0(1,:),'ydata',orbit_array0(2,:),'zdata',orbit_array0(3,:));
       set(hf_orbit2,'xdata',orbit_array2(1,:),'ydata',orbit_array2(2,:),'zdata',orbit_array2(3,:));
       set(hf1,'xdata',orbit_array1(1,end),'ydata',orbit_array1(2,end),'zdata',orbit_array1(3,end));
       set(hf2,'xdata',orbit_array2(1,end),'ydata',orbit_array2(2,end),'zdata',orbit_array2(3,end));
       set(hstick, 'XData', [orbit_array0(1,end) orbit_array1(1,end)], 'YData', [orbit_array0(2,end) orbit_array1(2,end)], 'ZData', [orbit_array0(3,end) orbit_array1(3,end)]);
       set(hvec, 'XData', [orbit_array0(1,end) orbit_array2(1,end)], 'YData', [orbit_array0(2,end) orbit_array2(2,end)], 'ZData', [orbit_array0(3,end) orbit_array2(3,end)]);

         set(hdashed2, 'XData', orbit_array0(1,end), ...
              'YData', orbit_array0(2,end), ...
              'ZData', orbit_array0(3,end), ...
              'UData', orbit_array2(1,end)-orbit_array0(1,end), ...
              'VData', orbit_array2(2,end)-orbit_array0(2,end), ...
              'WData', orbit_array2(3,end)-orbit_array0(3,end));
       set(lx);
       set(ly);
       set(lz);
       set(lxtext,'Interpreter', 'latex');
       set(lytext,'Interpreter', 'latex');
       set(lztext,'Interpreter', 'latex');
         % Update circle position
       center = 0.75*[orbit_array0(1,end) orbit_array0(2,end) orbit_array0(3,end)];
       v = null(orbit_array0(:,end)');
       points = repmat(center',1,size(theta0,2))+radius*(v(:,1)*cos(theta0)+v(:,2)*sin(theta0));
       set(hcirclefill, 'XData', points(1,:), 'YData', points(2,:), 'ZData', points(3,:));
       set(hcircleline, 'XData', points(1,:), 'YData', points(2,:), 'ZData', points(3,:));

       % Update title
       set(ht1,'Interpreter', 'latex','string',sprintf('$t$ = %0.2f s',t),'fontsize',30);
       % Capture the frame and write it to the video
       frame = getframe(gcf);
       writeVideo(vid, frame);

       pause(dt); % Time between t and t + dt, real-time pause(dt)
    end
    % Close the video writer
    close(vid);
end