data = dlmread('TV3_100Messungen.stat','',16,0);
x = data(:,1);
y = data(:,2);
E = dot(x,y)/sum(y); % Mittelwert
sigma = sqrt(dot(y,(x-E).^2)/sum(y));



bar(x,y,'FaceColor',[0.85 0.325 0.098], 'FaceAlpha', 1.0, 'BarWidth', 0.9)
hold on

x_plot=linspace(0,200,201);
f_gauss=350*normpdf(x_plot,E,sigma);
plot(x_plot,f_gauss,'r','LineWidth',2)
f_poisson = 200*poisspdf(x_plot,E);
plot(x_plot,f_poisson,'b','LineWidth',2)
ylim([0 10]);
xlabel('Anzahl der Zerf�lle pro 2s');
ylabel('H�ufigkeit');
title('Poissonverteilung und Messdaten der Radioaktivit�t');
legend('Messdaten','Normalverteilung','Poissonverteilung');
hold on

stem(E, 5)

