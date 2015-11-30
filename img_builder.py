# -*- coding: utf-8 -*-
import cStringIO

from PIL import Image

import helper
import helper_wm


def add_wm(url, imgpath, name, text, wz_img):
    buf = cStringIO.StringIO()
    helper.get_img(url, buf)
    im = Image.open(cStringIO.StringIO(buf.getvalue()))
    #print imgpath
    width, heigh = im.size
    if width > 1200:
        font_size = 30
    else:
        font_size = 25

    # 文字水印
    mark = helper_wm.text2img(text, font_size=font_size)
    # 叠加水印到图片
    image = helper_wm.watermark(im, mark, 'left_top', 0.7)
    if wz_img is not None:
        wz_im = Image.open(wz_img)
        wz_width, wz_heigh = wz_im.size
        if width < wz_width:
            wz_im.thumbnail((width, width))
            wz_width, wz_heigh = wz_im.size

        join_im = Image.new('RGBA', (width, heigh+wz_heigh))

        join_im.paste(image, (0, 0))
        join_im.paste(wz_im, (0, heigh))
        join_im.save(imgpath, 'JPEG')
    else:
        image.save(imgpath, 'JPEG')

def get_img_by_url(url, path, name, text, wz_img):
    """根据URL地址获取图片到本地并添加水印与合并违章路标图片"""
    try:
        imgpath = u'%s/%s.jpg' % (path, name)
        add_wm(url, imgpath, name, text, wz_img)
    except IOError as e:
        if e[0] == 2 or e[0] == 22:
            name = name.replace('*', '_').replace('?', '_').replace('|', '_').replace(
                '<', '_').replace('>', '_').replace('/', '_').replace('\\', '_')
            helper.makedirs(path)
            
            add_wm(url, imgpath, name, text, wz_img)
        else:
            imgpath = ''
            raise
    except Exception as e:
        raise
    finally:
        return imgpath
