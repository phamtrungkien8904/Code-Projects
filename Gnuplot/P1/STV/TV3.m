m = [0,2,5,6,4,1,0,0,0,0,0,0,0]/20*100;

x=linspace(0,12,13);
P=100*binopdf(x,12,0.22);
plot(x,P,'LineWidth',2,'Color','r')
hold on
stem(x,P,'LineWidth',2,'LineStyle','none','Color','r')
hold on 
plot(x,m,'LineWidth',2,'Color','b')
hold on
stem(x,m,'LineWidth',2,'LineStyle','--','Color','b')
xlabel('Erfolge')
ylabel('Wahrscheinlichkeit(%)')
xlim([0 12])
ylim([0 40])
legend('Binomialverteilung','','Messdaten','')