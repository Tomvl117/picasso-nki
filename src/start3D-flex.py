# -*- coding: utf-8 -*-
"""
Created on Wed Nov 29 13:05:37 2023

@author: t.v.leeuwen
"""

from pathlib import Path
import numpy as np
from picasso.unmixing import compute_unmixing_matrix
from skimage import io
import tifffile as tif
from skimage.util import img_as_float, img_as_uint
from skimage.transform import downscale_local_mean

indir = Path(r"/Volumes/1_DATA/Rheenen/tvl_jr/SP8/2024May2_SI_PFA_0.5mg_aio/")
outdir = Path(indir, 'output2')
if not outdir.exists():
    Path.mkdir(outdir)
rawImages = ['1', '2', '3', '4', '5'] # Filenames of the mixed images

ds = 4 # Downscale factor, default is 4

useCrop = True # Use a different image to derive unmixing values from
outputCrop = True # Also write the alternative images to file
cropImages = ['1-1', '2-1', '3-1', '4-1', '5-1'] # Filenames of the alternative images

for i in range(len(rawImages)):
    print("\nNow unmixing "+rawImages[i])
    
    img = img_as_float(io.imread(str(indir)+"/"+rawImages[i]+'.tif'))
    
    if len(img.shape) == 4:
        z_size = img.shape[0]
    else:
        z_size = 0
    
    if useCrop:
        crop = img_as_float(io.imread(str(indir)+"/"+cropImages[i]+'.tif'))
        if crop.shape[2] == min(crop.shape):
            crop = np.einsum('yxc->cyx', crop)
            print(crop.shape)
            if z_size > 0:
                img = np.einsum('zyxc->zcyx', img)
            else:
                img = np.einsum('yxc->cyx', img)
        
        mixed_downscaled = downscale_local_mean(crop, (1, ds, ds))
        mat_iters = compute_unmixing_matrix(
            mixed_downscaled, verbose=True, return_iters=True
        )
    else:
        if img.shape[2] == min(img.shape):
            if z_size > 0:
                img = np.einsum('zyxc->zcyx', img)
                mixed_downscaled = downscale_local_mean(img[0], (1, ds, ds))
            else:
                img = np.einsum('yxc->cyx', img)
                mixed_downscaled = downscale_local_mean(img, (1, ds, ds))
        else:
            if z_size > 0:
                mixed_downscaled = downscale_local_mean(img[0], (1, ds, ds))
            else:
                mixed_downscaled = downscale_local_mean(img, (1, ds, ds))
                
        mat_iters = compute_unmixing_matrix(
            mixed_downscaled, verbose=True, return_iters=True
        )
    
    unmixing_matrix = mat_iters[-1]
    print(unmixing_matrix)
    
    if z_size > 0:
        unmixed = []
    
        for z in range(z_size):
            unmixed.append(np.einsum('ij,jkl->ikl', unmixing_matrix, img[z]))
            np.clip(unmixed[z], 0, 1, out=unmixed[z])
    
        unmixed = np.asarray(unmixed)
    else:
        unmixed = np.einsum('ij,jkl->ikl', unmixing_matrix, img)
        np.clip(unmixed, 0, 1, out=unmixed)
    
    if useCrop and outputCrop:
        outCrop = np.einsum('ij,jkl->ikl', unmixing_matrix, crop)
        np.clip(outCrop, 0, 1, out=outCrop)
        tif.imwrite(str(outdir)+'/unmixed-'+cropImages[i]+'-ds'+str(ds)+'.tif', img_as_uint(outCrop))
    
    ## Save image
    tif.imwrite(str(outdir)+'/unmixed-'+rawImages[i]+'-ds'+str(ds)+'.tif', img_as_uint(unmixed))