x=linspace(0,40,41);
P=binopdf(x,40,0.5);
plot(x,P,'LineWidth',2,'Color','r')
hold on
stem(x,P,'LineWidth',2,'LineStyle','none','Color','r')
xlabel('Erfolge')
ylabel('Wahrscheinlichkeit')
legend('Binomialverteilung')