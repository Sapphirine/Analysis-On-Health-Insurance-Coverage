close all
clear 
%-------------PARAMETER DEFINITIONS---------------
%-------------------------------------------------
% Part1: plot the value of the K-means objective function
%-------------------------------------------------
% Step1: Data Loading
M_data = csvread('FL.csv');
data_size = size(M_data,1);
iterations = 5;
%-------------------------------------------------
% Step2: K-means implementation 
% Mean Assignment Step
k = 5;
mean_3 = M_data(randi([1,data_size],k,1),[2,4]); % 3 x 2 means for 3 clusters
% Cluster Updata Step
% -----------k=3-------------%
LL_3 = zeros(1,iterations);
C_3 = zeros(1,data_size);
for j = 1:iterations
    L = 0;
    for i = 1:data_size
        [M,I] = min(sum((bsxfun(@minus,M_data(i,[2,4]),mean_3)).^2,2)); % I: the index with the min dis
        L = L+M;
        C_3(i) = I;   % define the cluster of point i
    end
    mean_3 = [mean((M_data((find(C_3==1)),[2,4])));mean((M_data((find(C_3==2)),[2,4])));...
        mean((M_data((find(C_3==3)),[2,4])));mean((M_data((find(C_3==4)),[2,4])));mean((M_data((find(C_3==5)),[2,4])))];
    LL_3(j) = L;
end

%-------------------------------------------------
% Part2: plot final clusters for k=3,5
%-------------------------------------------------
c3_1 = (M_data((find(C_3==1)),[2,4]));
c3_2 = (M_data((find(C_3==2)),[2,4]));
c3_3 = (M_data((find(C_3==3)),[2,4]));
c3_4 = (M_data((find(C_3==4)),[2,4]));
c3_5 = (M_data((find(C_3==5)),[2,4]));
figure 
plot(c3_1(:,1),c3_1(:,2),'k+')
hold on
plot(c3_2(:,1),c3_2(:,2),'go')
hold on
plot(c3_3(:,1),c3_3(:,2),'b+')
hold on
plot(c3_4(:,1),c3_4(:,2),'co')
hold on
plot(c3_5(:,1),c3_5(:,2),'r*')
legend('k=1','k=2','k=3','k=4','k=5')
hold on
title('K-means Clustering on counties with uninsured rate and poverty rate in FL')
xlabel('uninsured rate')
ylabel('PPMCC coefficient')
