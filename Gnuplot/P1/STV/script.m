T = readtable('data.csv','HeaderLines',0,'ReadVariableNames',true);
m = T(:,2).';
n = 12;
p = 0.22;

x=linspace(0,n,n+1);
P=100*binopdf(x,n,p);
plot(x,P,'LineWidth',2,'Color','r')
hold on
stem(x,P,'LineWidth',2,'LineStyle','none','Color','r')
hold on 
plot(x,m,'LineWidth',2,'Color','b')
hold on
stem(x,m,'LineWidth',2,'LineStyle','--','Color','b')
xlabel('Erfolge')
ylabel('Wahrscheinlichkeit(%)')
xlim([0 n])
ylim([0 100])
legend('Binomialverteilung','','Messdaten','')