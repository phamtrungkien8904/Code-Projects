m = [0,2,1,4,9,6,8,2,0,0,0];

x=linspace(0,10,11);


plot(x,m,'LineWidth',2,'Color','b')
hold on
stem(x,m,'LineWidth',2,'LineStyle','--','Color','b')
xlabel('Kanal')
ylabel('Anzahl')
xlim([0 10])
ylim([0 10])
title('Kleine Statistik (32 Kugeln)')
legend('Messdaten','')


exportgraphics(gcf, 'TV1.eps', 'ContentType', 'vector');