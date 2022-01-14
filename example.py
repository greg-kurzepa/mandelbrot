import mandelbrot

#required arguments:

#  iterations per pixel,
#  image dimensions [width,height] in pixels,
#  x coordinate of centre,
#  y coordinate of centre,
#  radius

#optional arguments:

#  showImage (boolean) whether the image should be displayed when the render is done,
#  fileName (string) what name the file should be given (.png is automatically appended),
#  directory of the folder the file should be stored in (defaults to current working directory)

mandelbrot.render_img(500, [1920,1080], 0, 0, 2, showImage=True, fileName="my_image_1")
