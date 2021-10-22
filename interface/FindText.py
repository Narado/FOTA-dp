# -*-encoding=utf-8-*- #
import re
import pytesseract

import sys
from PIL import Image
sys.path.append("/InterceptPic.py")


class FindText:
    def __init__(self):
        pass

    def findtext(self,img): #传入图像对象
        """
        :param img: 提供图片对象
        :return:
        """
        text = pytesseract.image_to_string(img) #图片转文字
        print("图片转文字:",text)
        textj = re.sub(u"([^\u4e00-\u9fa5\u0030-\u0039\u0041-\u005a\u0061-\u007a])","", text) #去除识别出来的特殊字符
        textj_four = textj[0:4] #只获取前4个字符
        print("去除特殊字符，只取前4个字符：",textj_four)
        return textj_four

    #灰度处理，用convert把图片转成黑白色，设置threshold阈值，超过阈值的为黑色
    def processing_image(self,img):
        imgl = img.convert('L')
        pixdata = imgl.load()
        print("像素点：",pixdata)
        w,h=img.size
        threshold = 155
        for y in range(h):
            for x in range(w):
                if pixdata[x,y] < threshold:
                    pixdata[x,y] = 0
                else:
                    pixdata[x,y] = 250
        # imgl.show()
        return imgl

    #删除一些扰乱识别的像素点
    def delete_spot(self,images):
        data = images.getdata() #返回值是一个sequence对象，sequence对象的每一个元素对应一个像素点R、G、B值
        # str1 = list(data)
        # print(str1[0])
        # print(str1[1])
        # print(str1[2])
        # print(str1)
        # print(data[1*1+1])
        w, h = images.size
        black_point = 0
        for x in range(1, w-1):
            for y in range(1,h-1):
                mid_pixel = data[w*y+ x] #?为啥 这是中央像素点的像素值
                if mid_pixel <50 :
                    top_pixel = data[w*(y-1)+x]
                    left_pixel = data[w*y + (x-1)]
                    down_pixel = data[w*(y+1) +x]
                    right_pixel = data[w * y +(x+1)]
                    #判断上下左右的黑色像素点总个数
                    if top_pixel <10 :
                        black_point += 1
                    if left_pixel < 10:
                        black_point += 1
                    if down_pixel < 10:
                        black_point += 1
                    if right_pixel < 10:
                        black_point += 1
                    if black_point < 1:
                        images.putpixel((x, y), 255)
                    black_point = 0
        # images.show()
        return images


if __name__=='__main__':
    img = Image.open("C:\\Users\\lei.gao\\Desktop\\pic4.png")
    img2 = Image.open("C:\\Users\\lei.gao\\Desktop\\pic3.png")
    print("**********************图像处理前*********************\n")
    FindText().findtext(img)
    print("**********************图像处理后*********************\n")
    FindText().findtext(img2)
