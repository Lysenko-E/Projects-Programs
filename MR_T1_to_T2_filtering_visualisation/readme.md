\# T1 → T2 Like MRI Contrast Simulation (Educational Only)
---
This project demonstrates a simple, non clinical method for generating a \*\*T2 like contrast\*\* from a T1 weighted MRI image using basic image processing operations in Python. The goal is purely \*\*visualization and experimentation\*\*, not diagnostic accuracy or medical use.
The script loads a local MRI image, normalizes it, applies a gamma based contrast transformation to mimic T2 like characteristics, labels both images, displays them side by side in a comparison window, and saves the simulated output as `t2\_simulated.png`.
This was a project made out of curiosity, not for clinical use. 

\# Requirements

\- OpenCV (cv2): image loading, normalization, labeling, display, saving

\- NumPy: numerical operations and intensity transformations

No medical imaging libraries (SimpleITK, NiBabel, etc.) are required for this 2D demonstration.

! Please change the path inside the code to own location
---
Install the required Python libraries using the following:
```bash
pip install opencv-python numpy
```

---
What the Script Does
\- Loads a local MRI image in grayscale 512x512 provided in the folder
\- Normalizes intensities to a consistent 0–255 range
\- Applies a gamma based remapping to approximate T2 like contrast
\- Adds labels (“Original” and “T2 Simulated”) to each image
\- Displays both images side by side in a single OpenCV window
\- Saves the simulated T2 like image to disk
This is a visual filtering demonstration, not a physics based MRI simulation

\#Some explanations

T2 Like Contrast Method, The key transformation uses gamma correction:

```bash
t2\_mapped = np.power(img\_float, 0.6)
```
Why gamma = 0.6?

\- Gamma < 1 brightens dark regions. I found anything bellow 0.6 to bleach the image too much with 0.6 offering the best balance.

&nbsp;	CSF and fluid spaces appear brighter, similar to T2 weighted MRI.

\- Gamma mapping slightly darkens bright regions

&nbsp;	white matter becomes darker, another T2 like characteristic.

\- Midtones shift upward

&nbsp;	gray matter becomes more visible.

This produces a contrast profile that resembles T2 weighting without modeling T1/T2 relaxation physics.

---
Important Parameters Explained

cv2.normalize(img, None, 0.0, 1.0, cv2.NORM\_MINMAX)

\- Converts the image to a 0–1 float range

\- Ensures stable gamma behavior regardless of original intensity scale

np.power(img\_float, 0.6)

\- Main contrast transformation

\- Lower gamma → stronger T2 like effect

\- Adjustable depending on desired appearance

np.hstack((img\_labeled, t2\_labeled))

\- Combines both images horizontally for direct visual comparison

cv2.putText(...)

\- Adds labels directly onto each image for clarity


---
Disclaimer
This project is strictly for educational and visualization purposes.
\- It does not simulate true MRI physics
\- It does not model T1/T2 relaxation times
\- It is not a diagnostic tool
\- It must not be used for clinical decision making
The output is a visual approximation only, created using simple image processing filters.

**Reference**
The example T1‑weighted MRI image used in this project is based on a sagittal T1‑weighted scan showing normal midline brain structures.  
Original image and description courtesy of the MSD Manual Professional Edition and Hakan Ilaslan, MD:  
https://www.msdmanuals.com/professional/multimedia/image/t1-weighted-mri










