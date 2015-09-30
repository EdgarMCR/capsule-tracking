function [Sorted, max_distance] = Sort_points_into_polygon_cutoff(Points,cutoff_d)

Npoints = length(Points(:,1));
% Npoints
Sorted = zeros(Npoints+1,2);

max_distance = 0;

idx = 1;
for m=1:Npoints
    Sorted(m,:) = Points(idx,:);
    Working = Points(idx,:);
    
    Points = Points([1:idx-1,idx+1:end],:);
    Distance = (Points(:,1) - Working(1)).^2 + (Points(:,2) - Working(2)).^2;
    [d,idx] = min(Distance);
    if d>max_distance
        max_distance = d;
    end
    if d>cutoff_d^2

%         disp('Over cutoff distance');
        break;
    end
       
end
        Sorted = Sorted(1:m,:);
% [d, cutoff_d^2]
% idx
% max_distance = sqrt(max_distance);
% if length(idx)==0 | d<cutoff_d^2  
%     disp('Closing loop');
%     Sorted(end,:) = Sorted(1,:);
% end