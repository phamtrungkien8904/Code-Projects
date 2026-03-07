x=linspace(0,40,41);
P=100*binopdf(x,40,0.5);
plot(x,P,'LineWidth',2,'Color','r')
hold on
stem(x,P,'LineWidth',2,'LineStyle','none','Color','r')
xlabel('Erfolge')
ylabel('Wahrscheinlichkeit')
xlim([0 40])
ylim([0 100])
legend('Binomialverteilung')