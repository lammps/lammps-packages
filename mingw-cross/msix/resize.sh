#!/bin/bash

SquareLogo=lammps-logo-square.png
WideLogo=Logo_w_text_black_wide.png
StoreLogo=Logo_w_text_black.png

convert $SquareLogo -resize 16x16   Assets/Square44x44Logo.targetsize-16.png
convert $SquareLogo -resize 16x16   Assets/Square44x44Logo.targetsize-16_altform-unplated.png
convert $SquareLogo -resize 24x24   Assets/Square44x44Logo.targetsize-24.png
convert $SquareLogo -resize 24x24   Assets/Square44x44Logo.targetsize-24_altform-unplated.png
convert $SquareLogo -resize 32x32   Assets/Square44x44Logo.targetsize-32.png
convert $SquareLogo -resize 32x32   Assets/Square44x44Logo.targetsize-32_altform-unplated.png
convert $SquareLogo -resize 48x48   Assets/Square44x44Logo.targetsize-48.png
convert $SquareLogo -resize 48x48   Assets/Square44x44Logo.targetsize-48_altform-unplated.png
convert $SquareLogo -resize 256x256 Assets/Square44x44Logo.targetsize-256.png
convert $SquareLogo -resize 256x256 Assets/Square44x44Logo.targetsize-256_altform-unplated.png

convert $SquareLogo -resize 44x44   Assets/Square44x44Logo.scale-100.png
convert $SquareLogo -resize 55x55   Assets/Square44x44Logo.scale-125.png
convert $SquareLogo -resize 66x66   Assets/Square44x44Logo.scale-150.png
convert $SquareLogo -resize 88x88   Assets/Square44x44Logo.scale-200.png
convert $SquareLogo -resize 176x176 Assets/Square44x44Logo.scale-400.png

convert $SquareLogo -resize 71x71   Assets/Square71x71Logo.scale-100.png
convert $SquareLogo -resize 89x89   Assets/Square71x71Logo.scale-125.png
convert $SquareLogo -resize 107x107 Assets/Square71x71Logo.scale-150.png
convert $SquareLogo -resize 142x142 Assets/Square71x71Logo.scale-200.png
convert $SquareLogo -resize 284x284 Assets/Square71x71Logo.scale-400.png

convert $SquareLogo -resize 150x150 Assets/Square150x150Logo.scale-100.png
convert $SquareLogo -resize 188x188 Assets/Square150x150Logo.scale-125.png
convert $SquareLogo -resize 225x225 Assets/Square150x150Logo.scale-150.png
convert $SquareLogo -resize 300x300 Assets/Square150x150Logo.scale-200.png
convert $SquareLogo -resize 600x600 Assets/Square150x150Logo.scale-400.png

convert $SquareLogo -resize 310x310   Assets/Square310x310Logo.scale-100.png
convert $SquareLogo -resize 388x388   Assets/Square310x310Logo.scale-125.png
convert $SquareLogo -resize 465x465   Assets/Square310x310Logo.scale-150.png
convert $SquareLogo -resize 620x620   Assets/Square310x310Logo.scale-200.png
convert $SquareLogo -resize 1240x1240 Assets/Square310x310Logo.scale-400.png

convert $WideLogo -resize 310x150   Assets/Wide310x150Logo.scale-100.png
convert $WideLogo -resize 388x188   Assets/Wide310x150Logo.scale-125.png
convert $WideLogo -resize 465x225   Assets/Wide310x150Logo.scale-150.png
convert $WideLogo -resize 620x300   Assets/Wide310x150Logo.scale-200.png
convert $WideLogo -resize 1240x600  Assets/Wide310x150Logo.scale-400.png

convert $StoreLogo -resize 256x256  Assets/StoreLogo.png
convert $StoreLogo -resize 50x50    Assets/StoreLogo.scale-100.png
convert $StoreLogo -resize 63x63    Assets/StoreLogo.scale-125.png
convert $StoreLogo -resize 75x75    Assets/StoreLogo.scale-150.png
convert $StoreLogo -resize 100x100  Assets/StoreLogo.scale-200.png
convert $StoreLogo -resize 200x200  Assets/StoreLogo.scale-400.png
