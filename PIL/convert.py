import Image
import time
import sys

start = time.time()
im = Image.open(sys.argv[1])
print "Open -> %s" % (time.time()-start)

RGB_from = (0,63, 83)
RGB_to = (184, 187, 164)


matrix = list()

conv_func = lambda (l, r, p): int(l+(r-l)/255.0*p)

start = time.time()
for i in range(0, 256):
    #matrix.append(conv_func(RGB_from[0], RGB_to[0], i))
    matrix.extend( map(conv_func, zip(RGB_from, RGB_to, (i,i,i))) )
#print matrix
print "Matrix build -> %s" % (time.time()-start)

start = time.time()
out = im.convert('L')
print "Convert to L -> %s" % (time.time()-start)

start = time.time()
out.putpalette(matrix)
print "Put paletet -> %s" % (time.time()-start)

start = time.time()
out = out.convert('RGB')
print "Convert RGB -> %s" % (time.time()-start)

start = time.time()
out.save('conv-' + sys.argv[1])
print "Save -> %s" % (time.time()-start)

