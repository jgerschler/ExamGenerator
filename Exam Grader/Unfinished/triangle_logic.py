triangles = [(0, 523, 527, 3196.0), (1, 69, 527, 3196.0),
             (2, 175, 403, 4044.0), (3, 340, 139, 1153.0),
             (4, 524, 71, 3196.0), (5, 70, 71, 3196.0)]

def filter_triangles(t_list):
    markers = []
    t_list.sort(key=lambda x: x[3])
    
    for i in range(len(t_list) - 1):       
        
        if (t_list[i + 1][3] >= t_list[i][3] * 0.95 and
            t_list[i + 1][3] <= t_list[i][3] * 1.05):

            markers.append(t_list[i + 1])

    if len(markers) != 4:
        print("Error: Markers != 4")
        return markers

    return markers
