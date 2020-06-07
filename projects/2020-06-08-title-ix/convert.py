
"""
  Converts a PDF file to a PNG file.

  Setup:
  - Install ghostscript and imagemagick.

  Steps:
  mkdir images
  convert -density 100 TitleIX.pdf images/TitleIX.png
  # delete first page
  rm images/TitleIX-0.png
  # append pages to get final image
  convert -append images/TitleIX*.png final.png

  https://superuser.com/questions/290656/combine-multiple-images-using-imagemagick

  # convert *append images/TitleIX*.png out.png # concat horizontal
"""
