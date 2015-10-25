# -*- coding: utf-8 -*-

from PIL import Image, ImageEnhance, ImageDraw, ImageFont

def text2img(text, font_color="White", font_size=25):
    """生成内容为 TEXT 的水印"""

    #font = ImageFont.truetype('simsun.ttc', font_size)
    font = ImageFont.truetype('WRYH.ttf', font_size)
    #多行文字处理
    text = text.split('\n')
    mark_width = 0
    for  i in range(len(text)):
        (width, height) = font.getsize(text[i])
        if mark_width < width:
            mark_width = width
    mark_height = height * len(text)
    #print 'mark_width: %s' % mark_width
    #print 'mark_height: %s' % mark_height

    #生成水印图片
    mark = Image.new('RGBA', (mark_width, mark_height), color = (0, 0, 0))
    draw = ImageDraw.ImageDraw(mark, "RGBA")
    draw.setfont(font)
    for i in range(len(text)):
        (width, height) = font.getsize(text[i])
        draw.text((0, i*height), text[i], fill=font_color)
    return mark

def set_opacity(im, opacity):
    """设置透明度"""

    assert opacity >=0 and opacity < 1
    if im.mode != "RGBA":
        im = im.convert('RGBA')
    else:
        im = im.copy()
    alpha = im.split()[3]
    alpha = ImageEnhance.Brightness(alpha).enhance(opacity)
    im.putalpha(alpha)
    return im

def watermark(im, mark, position, opacity=1):
    """添加水印"""

    try:
        if opacity < 1:
            mark = set_opacity(mark, opacity)
        if im.mode != 'RGBA':
            im = im.convert('RGBA')
        if im.size[0] < mark.size[0] or im.size[1] < mark.size[1]:
            print "The mark image size is larger size than original image file."
            return False

        #设置水印位置
        if position == 'left_top':
            x = 0
            y = 0
        elif position == 'left_bottom':
            x = 0
            y = im.size[1] - mark.size[1]
        elif position == 'right_top':
            x = im.size[0] - mark.size[0]
            y = 0
        elif position == 'right_bottom':
            x = im.size[0] - mark.size[0]
            y = im.size[1] - mark.size[1]
        else:
            x = (im.size[0] - mark.size[0]) / 2
            y = (im.size[1] - mark.size[1]) / 2

        layer = Image.new('RGBA', im.size,)
        layer.paste(mark,(x,y))
        return Image.composite(layer, im, layer)
    except Exception as e:
        print ">>>>>>>>>>> WaterMark EXCEPTION:  " + str(e)
        #return False
        raise

def main():
    #text = u'Linsir.水印.\nvi5i0n@hotmail.comLinsir.水印.\nvi5i0n@hotmail.comLinsir.水印.\nvi5i0n@hotmail.comLinsir.水印.\nvi5i0n@hotmail.com'
    text = u'Linsir.水印.vi5i0n@hotmail.com'
    # text = open('README.md').read().decode('utf-8')
    # print text
    im = Image.open('test2.jpg')
    mark = text2img(text)
    image = watermark(im, mark, 'left_top', 0.7)
    if image:
        image.save('watermark2.jpg')
    else:
        print "Sorry, Failed."


if __name__ == '__main__':
    main()
