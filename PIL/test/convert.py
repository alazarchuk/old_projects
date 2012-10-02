import Image
import time
import sys
import os

#start = time.time()
#im = Image.open(sys.argv[1])
#print "Open -> %s" % (time.time()-start)

#RGB_from = (0,63, 83)
#RGB_to = (184, 187, 164)


#matrix = list()

#conv_func = lambda (l, r, p): int(l+(r-l)/255.0*p)

#start = time.time()
#for i in range(0, 256):
    #matrix.extend( map(conv_func, zip(RGB_from, RGB_to, (i,i,i))) )

#print "Matrix build -> %s" % (time.time()-start)

#start = time.time()
#out = im.convert('L')
#print "Convert to L -> %s" % (time.time()-start)

#start = time.time()
#out.putpalette(matrix)
#print "Put paletet -> %s" % (time.time()-start)

#start = time.time()
#out = out.convert('RGB')
#print "Convert RGB -> %s" % (time.time()-start)

#start = time.time()
#out.save('conv-' + sys.argv[1])
#print "Save -> %s" % (time.time()-start)

pr_name = os.path.basename(sys.argv[1]) + "_f"
img_dir = os.path.join(pr_name, "img")

tmp_img = os.path.join(img_dir, "temp.tiff")

os.makedirs(img_dir)

os.system("gs -dNOPAUSE -dBATCH -dSAFER -sDEVICE=tiffgray -r200  -sOutputFile=%s -q %s" % (tmp_img, sys.argv[1])) 

RGB_from = (0,63, 83)
RGB_to = (184, 187, 164)
matrix = list()
conv_func = lambda (l, r, p): int(l+(r-l)/255.0*p)
for i in range(0, 256):
    matrix.extend( map(conv_func, zip(RGB_from, RGB_to, (i,i,i))) )


class ImageSequence:
    def __init__(self, im):
        self.im = im
    def __getitem__(self, ix):
        try:
             if ix:
                 self.im.seek(ix)
             return (ix, self.im)
        except EOFError:
             self.im.seek(0)
             raise IndexError # end of sequence

im = Image.open(tmp_img)

img_list = list()

for (idx, frame) in ImageSequence(im):
    frame.putpalette(matrix)
    frame_r = frame.convert('RGB')
    img_name = "img_%s.jpg" % str(idx).zfill(4)
    img_name = os.path.join('img', img_name)
    img_list.append(img_name)
    frame_r.save(os.path.join(pr_name, img_name))
    
    
html_head = """
<html>
<head>
<title>%s</title>
</head>
<body style="background-color: rgb(211, 211, 211);">
""" % (pr_name, )

html_end = """
</body>
</html>
"""

img_tmpl = """
<img style="border: 2px solid ; width: 100%%;"
src="%s">
<br>
<br>
<br>
<br>
"""

fd = open(os.path.join(pr_name, "%s.html" % pr_name), "wb")
fd.write(html_head)
for img_path in img_list:
    fd.write(img_tmpl % img_path)
fd.write(html_end)
fd.close()

os.remove(tmp_img)
