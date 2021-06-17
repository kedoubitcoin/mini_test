# coding=utf-8
import binascii
import PIL
import numpy as np
import usb.core
import time

from PIL import Image

# def encode_pixels(img):
#     r = ""
#     img = [(x[0] + x[1] + x[2] > 384 and "1" or "0") for x in img]
#     for i in range(len(img) // 8):
#         c = "".join(img[i * 8 : i * 8 + 8])
#         r += "0x%02x, " % int(c, 2)
#     return r
def encode_color_pixels(img):
    r = ""
    for x in img:
        r_data = (x[0]<<16 & 0x00ff0000) >>19
        g_data = (x[1]<<8 & 0x0000ff00) >>10
        b_data = (x[2] & 0x000000ff) >>3
        rgb565_data = (r_data <<11) + (g_data << 5) + (b_data << 0)
        # print(rgb565_data)
        d1 = rgb565_data >>8
        d2 = rgb565_data & 0x00ff
        r += "%02x " % d1
        r += "%02x " % d2
        # print(r)
    return r
#制作图像
# image = Image.new('RGB', (128, 128), (120, 120, 255))
# image.show()
# image.save("/Users/jiyajie/Pictures/test1.png")

#将PNG转换为jpg
# img = Image.open("/Users/jiyajie/Pictures/chrome.png")
# print(img.mode)
#
# img_pil = img.convert('RGBA')
# x, y = img.size
# img_jpg = Image.new("RGBA", img.size, (255,255,255))
# img_jpg.paste(img_pil, (0, 0, x, y), img_pil)
# img_jpg = img_jpg.convert("RGB")
# print(img_jpg.mode, img_jpg.size)
# img_jpg.save("/Users/jiyajie/Pictures/chrome-1.jpg")

img = Image.open("/Users/jiyajie/Pictures/chrome-1.jpg")
img_data = list(img.getdata())
data = encode_color_pixels(img_data)
data_len = len(data)
print(data_len)

#保存为txt文件
# f = open("/Users/jiyajie/Pictures/chrome-1.txt",'a')
# f.write(data)

send_lenth = ''
len1 = data_len >> 16
len2 = (data_len >>8) & 0x00ff
len3 = data_len &0x00ff
send_lenth += "0x%02x, " % len1
send_lenth += "0x%02x, " % len2
send_lenth += "0x%02x, " % len3
print(send_lenth)


# #
# lena = Image.open("/Users/jiyajie/Pictures/test1.png")
# print(lena.mode)
# print(lena.getpixel((0,0)))
# lena.show()
#
# r, g, b = lena.split()  # 分离三通道
# print(r)
# print(g)
# print(b)

# #USB识别
VID = 0x1209
PID = 0x53c0

dev = usb.core.find(idVendor=VID, idProduct=PID)

# was it found?
if dev is None:
    raise ValueError('Device not found')

cfg = dev.get_active_configuration()
intf = cfg[(0, 0)]
print(intf)

ep = usb.util.find_descriptor(
    intf,
    # match the first OUT endpoint
    custom_match = \
    lambda e: \
        usb.util.endpoint_direction(e.bEndpointAddress) == \
        usb.util.ENDPOINT_OUT)

assert ep is not None
#
msg_getfeatures = '3f 23 23 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 '
msg_flashstart =  '3f 23 23 00 06 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 '
msg_flashlen =  '3f 23 23 00 07 00 82 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 '
send_data1 = bytes.fromhex(msg_getfeatures)
send_data2 = bytes.fromhex(msg_flashstart)
send_data3 = bytes.fromhex(msg_flashlen)
# print(send_data)
dev.write(1,send_data1,1000)  #write(endpoint, data, timeout = None)
resp = dev.read(0x81,64,1000)
print(resp)
dev.write(1,send_data2,1000)
resp = dev.read(0x81,64,1000)
print(resp)
dev.write(1,send_data3,1000)
# resp = dev.read(0x81,64,1000)
# print(resp)≤

# type = type(data)
# print(type)

#test data
# data = '30 31 32 33 34 35 36 37 38 39 30 31 32 33 34 35 36 37 38 39 30 31 32 33 34 35 36 37 38 39 30 31 32 33 34 35 36 37 38 39 30 31 32 33 34 35 36 37 38 39 30 31 32 33 34 35 36 37 38 39 30 31 32 33 \
# 30 31 32 33 34 35 36 37 38 39 30 31 32 33 34 35 36 37 38 39 30 31 32 33 34 35 36 37 38 39 30 31 32 33 34 35 36 37 38 39 30 31 32 33 34 35 36 37 38 39 30 31 32 33 34 35 36 37 38 39 30 31 32 33 \
# 30 31 32 33 34 35 36 37 38 39 30 31 32 33 34 35 36 37 38 39 30 31 32 33 34 35 36 37 38 39 30 31 32 33 34 35 36 37 38 39 30 31 32 33 34 35 36 37 38 39 30 31 32 33 34 35 36 37 38 39 30 31 32 33 \
# 30 31 32 33 34 35 36 37 38 39 30 31 32 33 34 35 36 37 38 39 30 31 32 33 34 35 36 37 38 39 30 31 32 33 34 35 36 37 38 39 30 31 32 33 34 35 36 37 38 39 30 31 32 33 34 35 36 37 38 39 30 31 32 33 \
# 30 31 32 33 34 35 36 37 38 39 30 31 32 33 34 35 36 37 38 39 30 31 32 33 34 35 36 37 38 39 30 31 32 33 34 35 36 37 38 39 30 31 32 33 34 35 36 37 38 39 30 31 32 33 34 35 36 37 38 39 30 31 32 33 \
# 30 31 32 33 34 35 36 37 38 39 30 31 32 33 34 35 36 37 38 39 30 31 32 33 34 35 36 37 38 39 30 31 32 33 34 35 36 37 38 39 30 31 32 33 34 35 36 37 38 39 30 31 32 33 34 35 36 37 38 39 30 31 32 33'
# data_len = (len(data))
# print(data_len)
#end test data


msg_head1 = '3'
msg_head2 = 'f'
msg_head3 = ' '
list_data = list(data)
# print(type(list_data))

i=0
list_data_len = data_len+int((data_len/189))*3
last_len = list_data_len%192
# print(list_data_len)
while i < list_data_len:
    # print(i)
    list_data.insert(i, msg_head1)
    list_data.insert(i+1, msg_head2)
    list_data.insert(i+2, msg_head3)
    # print(list_data[i:i + 192])
    i += 192

lenth_append = 192-last_len
while (lenth_append):
    list_data.append('0')
    list_data.append('0')
    list_data.append(' ')
    lenth_append -=3
# print(list_data)
# print(len(list_data))

pos = 0
list_data_len = len(list_data)-3
while pos < (list_data_len):
    print(pos)
    back_list_data = list_data[pos:pos+192]
    # print(back_list_data)
    send_data4 = ''.join(back_list_data)
    # print(send_data4)
    send_data4 = bytes.fromhex(send_data4)
    print(send_data4)
    data = dev.write(1, send_data4, 1000)
    # resp = dev.read(0x81, 64, 1000)
    # print(resp)
    pos += 192
    send_data4 = ''

    # if pos >= 98688 :
    #     print(back_list_data)
    #     print(send_data4)

# print(type(send_data4))
# send_lenth = len(send_data4)
# print(send_lenth)
# print(send_data4)