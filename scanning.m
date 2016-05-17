%===============Data Scanning=================%
% ensure the csv file is in the same directory 
function [interested2] = scanning(state,percent)

    M_data = csvread(strcat(state,'.csv'));
    %M_data = csvread('FL.csv');
    data_size = size(M_data,1);
    num = int8(0.1*data_size);  % number of points interested
    count = zeros(1,data_size);
    for i=1:data_size
        for j = 1:data_size
            if (M_data(i,2)<M_data(j,2)) && (M_data(i,4)<M_data(j,4))
                count(i) = count(i) + 1;
            end
        end
    end
    
    selected = M_data(find(count==num),:);
    
    [x,idx] = max(selected(:,2)); % idx=5
    threshold = selected(idx,:);
    interested1 = M_data((M_data(:,2)>threshold(2)),:);
    interested2 = interested1(interested1(:,4)>threshold(4),:);
    interested3 = interested2(interested2(:,4)>0,:);
    csvwrite(strcat(state,'_i.csv'),interested3)
    %csvwrite(strcat('FL_i.csv'),interested3)
    figure 
    plot(M_data(:,2),M_data(:,4),'b+')
    hold on
    plot(interested3(:,2),interested3(:,4),'ro')
    legend('all','interested')
    title('Automatic Searching on the first 10% rich people who are not covered by insurance')
    xlabel('uninsured rate')
    ylabel('PPCMM coefficient')
end