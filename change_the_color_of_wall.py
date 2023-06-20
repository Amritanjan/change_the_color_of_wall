import cv2
import numpy as np


def threshole_base_selected_pix(img,seed,color_to_change):
    pixel_value = img[seed[0], seed[1]]
    B_upper_cut, G_upper_cut, R_upper_cut = pixel_value
    
    max_num=min(B_upper_cut,G_upper_cut,R_upper_cut)

    R,G,B=cv2.split(img)
    
    if(max_num==B_upper_cut):
        plane=B
        (ret, mask) = cv2.threshold(B, 0, 255, cv2.THRESH_BINARY_INV+cv2.THRESH_OTSU)
        print("blue")
    elif(max_num==G_upper_cut):
        plane=G
        (ret, mask) = cv2.threshold(G, 0, 255, cv2.THRESH_BINARY_INV+cv2.THRESH_OTSU)
        print("green")
    else:
        (ret, mask) = cv2.threshold(R, 0, 255, cv2.THRESH_BINARY_INV+cv2.THRESH_OTSU)
        plane=R
        print("red")
    
    
    pixel_value_gray = mask[seed[0], seed[1]]
    if(pixel_value_gray==0):
        mask=cv2.bitwise_not(mask)

    foreground_list=[]
    background_list=[]

    pts1 = np.where(mask == 255)
    pts2 = np.where(mask == 0)

    foreground_list.append(plane[pts1[0], pts1[1]])
    background_list.append(plane[pts2[0], pts2[1]])
    

    median_f=round(np.median(foreground_list) ,2)
    mean_f=round(np.mean(foreground_list) ,2)
    std_dev_f=round(np.std(foreground_list) ,2)

    median_b=round(np.median(background_list),2)
    mean_b=round(np.mean(background_list),2)
    std_dev_b=round(np.std(background_list) ,2)

    print("foreground ",mean_f,",",median_f,",",std_dev_f)
    print("backgroundground ",mean_b,",",median_b,",",std_dev_b)
    
    per=((max(mean_f,mean_b)-min(mean_f,mean_b))/max(mean_f,mean_b))
    print("per=",per)
    if(per<=0.2):
        img[mask ==0] = color_to_change

    img[mask == 255] = color_to_change
    #cv2.imshow("mask",mask)
    #cv2.imshow("img_out",img)
    #cv2.waitKey(1)
    return(img)








def on_mouse(event, x, y, flags, params):
    if event == cv2.EVENT_LBUTTONDOWN: 
        print( 'Seed: ' + str(x) + ', ' + str(y), image[y,x])
        clicks.append((y,x))
    

def on_mouse_2(event, x, y, flags, params):
    if event == cv2.EVENT_LBUTTONDOWN: 
        print( 'color: ' + str(x) + ', ' + str(y), image_color[y,x])
        clolor_list.append((y,x))
    

        
clicks = []
clolor_list=[]

image = cv2.imread('/home/amritanjan/Downloads/wall_color_change/1.jpeg')

cv2.namedWindow('Input')
cv2.setMouseCallback('Input', on_mouse, 0, )
cv2.imshow('Input', image)

image_color=cv2.imread("color.jpg")
cv2.namedWindow('color_select')
cv2.setMouseCallback('color_select', on_mouse_2, 0, )
cv2.imshow('color_select', image_color)

cv2.waitKey()
seed = clicks[-1]
color=clolor_list[-1]
color_to_change = image_color[color[0], color[1]]
print(color_to_change)
out = threshole_base_selected_pix(image.copy(),seed,color_to_change)
final=cv2.hconcat([image,out])

cv2.imshow('input', out)
cv2.imshow('final', final)

cv2.waitKey()
cv2.destroyAllWindows()