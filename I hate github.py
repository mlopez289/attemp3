# -*- coding: utf-8 -*-
"""
Created on Thu Apr 23 00:05:33 2020

@author: Matias
"""

# -*- coding: utf-8 -*-
"""
Created on Wed Apr 22 15:32:31 2020

@author: matias!
"""
import numpy as np

  #How far is away is the camera?
L = 2.0E-3
  #Which modes are we exciting? Using the values pulled from water resonance notes
n = 1
m = 2
  #Setting quality factor, applied force, eff spring const and pool length
Q = 10.0
F = 3.0E-09
kappa = 0.95    
a = 5.0E-3
  #calculating the angle now (Assuming x = a/2 & y = b/2)
'''
  This is what bothers me, using the values n=1 & m=2 should result in 'trig' being zero, but instead I get a value
  that isn't zero but eventually returns the displacement you calculated in the Water Resonance notes, but off by
  a factor of 10^-33. Using n=2 & m=1 (which feels more correct since it means sine and cosine will be one) instead
  gives a wildy wrong answer. help!
'''
trig = np.cos((n/2)*np.pi)*np.sin((m/2)*np.pi)
angle = (Q*F*n*np.pi*trig)/(kappa*a)
  #calculating the estimated displacment:
d = 2*angle*L

  #for later use once I can calculate your value of 5μm from the notes
def camera_simulation(img, bit_depth=8, gain=0, black_level=1, dark_noise=3.71, gain16=2.89):
    '''
    Compute a simulated image from a CMOS/CCD camera.
    Adds dark and shot noise, but not non-linearity or fixed pattern noise.

    Parameters
    ----------
    img : 2D numpy array
        Input image, with brightness specified in electrons.  The maximum
        possible brightness should be 2**16 / gain16 / 10**(gain/20).
        With default conditions this is ~22,700.

    Keywords
    --------
    bit_depth : int (default: 8)
        The bit depth of the output image; typically 8, 12, or 16.
    gain : float (default: 0)
        The readout gain in dB.  Usually 0--40 or 0--20, depending on the camera.
        For maximum noise performance, this is typically left at 0.  This has
        the same effect as setting the `Gain` attribute on the camera.
    black_level : float (defaul: 1)
        The black level in percent.  Has the same effect as setting the
        `BlackLevel` attribute on the camera.
    dark_noise : float (default: 3.71)
        The per-pixel dark noise in electrons.  Typically 2--20.
    gain16 : float (default: 2.89)
        The camera readout gain in DU / e-, assuming 16 bit depth.  For FLIR
        camera (formerly PointGrey), this is typically 1--10.  If your docs
        specify a number less than 1, this is the *recipricol* of this number.
        Note: this number should not change if you reduce the bit depth;
        leave it as is, and the code will take care of it.
    '''
    bit_depth = int(bit_depth)
    if (bit_depth > 16) or (bit_depth < 8):
        raise ValueError('bit_depth must be between 8 and 16.')

    noise = np.random.randn(*img.shape) * np.sqrt(dark_noise**2 + img)
    max = 2**16 - 1
    bl = max * black_level/100
    img_u = np.clip((img + noise) * gain16 * 10**(gain/20) + bl, 0, max).astype('u2')
    img_u >>= (16 - bit_depth)

    if bit_depth == 8:
        return img_u.astype('u1')
    else: return img_u << (16 - bit_depth)
