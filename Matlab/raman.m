x = linspace(-1000,1000,2001);
y = 100/0.4*normpdf(x,-500,10) + 130/0.4*normpdf(x,0,10) + 10/0.4*normpdf(x,500,10);

plot(x,y,'LineWidth',2,'Color','r','LineStyle','-')

xlabel('Raman-Verschiebung (cm)')
ylabel('Raman-Intensität (arb. u.)')
xlim([-1000 1000])
ylim([0 15])
title('Raman-Spektrum')
legend('\lambda = 514 nm')
grid on