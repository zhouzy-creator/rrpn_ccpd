import os



provinces = ['皖', '沪', '津', '渝', '冀', '晋', '蒙', '辽', '吉', '黑', '苏', '浙', '京', '闽', '赣', '鲁', '豫', '鄂',
'湘', '粤', '桂', '琼', '川', '贵', '云', '藏', '陕', '甘', '青', '宁', '新', '警', '学', 'O']

alphabets = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'J', 'K', 'L', 'M', 'N', 'P', 'Q', 'R', 'S', 'T', 'U', 'V', 'W',
'X', 'Y', 'Z', 'O']

ads = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'J', 'K', 'L', 'M', 'N', 'P', 'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X',
'Y', 'Z', '0', '1', '2', '3', '4', '5', '6', '7', '8', '9', 'O']

gt_text_dir="./"
gt_img_dir="./"
def STRcoordinates_deal(STRcoordinates,i):
    # STRcoordinates = STRcoordinates.split('_')
    result = STRcoordinates[i]
    x,y = int(result.split('&')[0]),int(result.split('&')[1])
    result = x,y
    return result



def analyse_file(filename):
    STRinformation = filename.split('-')
    STRarea_ratio = STRinformation[0]
    STRangle = STRinformation[1]
    STRcoordinates = STRinformation[3]  #386&473_177&454_154&383_363&402 右下、左下、左上、右下
    STRchars = STRinformation[4]

    #坐标处理
    coordinates = []
    STRcoordinates = STRcoordinates.split('_')
    right_bottom = STRcoordinates_deal(STRcoordinates,0)
    left_top = STRcoordinates_deal(STRcoordinates,1)
    left_bottom = STRcoordinates_deal(STRcoordinates,2)
    right_top = STRcoordinates_deal(STRcoordinates,3)
    coordinates = [right_bottom,left_top,left_bottom,right_top]

    #车牌字符处理
    LPchars = []
    STRchars = STRchars.split('_')
    LPchars.append(provinces[int(STRchars[0])])
    LPchars.append(alphabets[int(STRchars[1])])
    for i in range(2,7):
        LPchars.append(ads[int(STRchars[i])])

    return coordinates,LPchars

def write_gt( fname,cords,info ):
    start = bytes([0xef,0xbb,0xbf])
    with open(os.path.join(gt_text_dir, fname),"wb") as f:
        line =str(cords[0][0])+","+str(cords[0][1])+","+\
         str(cords[1][0]) + "," + str(cords[1][1])+","+\
        str(cords[2][0]) + "," + str(cords[2][1])+","+\
        str(cords[3][0]) + "," + str(cords[3][1]) + "," + "".join(info)
        f.write (start)

        f.write(line.encode(encoding="utf-8"))




dirs = os.listdir(gt_img_dir)
for f in dirs:
    if (f.endswith(".jpg")):
        print(f)
        img_name = f[0:-4]
        print(img_name)
        img_gt_text_name = "gt_" + img_name + ".txt"
        cords, info =analyse_file(f)
        write_gt(img_gt_text_name,cords,info)