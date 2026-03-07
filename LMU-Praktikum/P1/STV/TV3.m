m = [0,2,5,6,4,1,0,0,0,0,0,0,0]/20*100;

x=linspace(0,12,13);
P_bi=100*binopdf(x,12,0.22);
P_poi=100*poisspdf(x,12*0.22);

plot(x,P_bi,'LineWidth',2,'Color','r')
hold on
plot(x,P_poi,'LineWidth',2,'Color','g')
hold on
stem(x,P_bi,'LineWidth',2,'LineStyle','none','Color','r')
hold on 
plot(x,m,'LineWidth',2,'Color','b')
hold on
stem(x,m,'LineWidth',2,'LineStyle','--','Color','b')
xlabel('Erfolge')
ylabel('Wahrscheinlichkeit(%)')
xlim([0 12])
ylim([0 40])
title('Messdaten vs. Theorie')
legend('Binomialverteilung','Poissonverteilung','','Messdaten','')


exportgraphics(gcf, 'data.eps', 'ContentType', 'vector');