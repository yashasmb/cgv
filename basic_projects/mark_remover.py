"""Demo of OpenCV inpainting.

Run using: python3 5_imageInpainting.py image.jpg

Where image.jpg is a relative or absolute path to an image file.
"""

import numpy as np
import cv2
import sys
import argparse


class Sketcher:
    """OpenCV Utility class for mouse handling."""

    def __init__(self, windowname, dests, colors_func):
        self.prev_pt = None
        self.windowname = windowname
        self.dests = dests
        self.colors_func = colors_func
        self.dirty = False
        self.show()
        cv2.setMouseCallback(self.windowname, self.on_mouse)

    def show(self):
        cv2.imshow(self.windowname, self.dests[0])
        cv2.imshow(self.windowname + ": mask", self.dests[1])

    def on_mouse(self, event, x, y, flags, param):
        """Hanles mouse movement and events."""
        pt = (x, y)
        if event == cv2.EVENT_LBUTTONDOWN:
            self.prev_pt = pt
        elif event == cv2.EVENT_LBUTTONUP:
            self.prev_pt = None

        if self.prev_pt and flags & cv2.EVENT_FLAG_LBUTTON:
            for dst, color in zip(self.dests, self.colors_func()):
                cv2.line(dst, self.prev_pt, pt, color, 5)
            self.dirty = True
            self.prev_pt = pt
            self.show()


def main():
    """Runs the main execution loops for inpainting."""
    args = argparse.ArgumentParser(description='image_path')
    args.add_argument("image", type=str)

    print("Usage: python inpaint <image_path>")
    print("Keys: ")
    print("t - inpaint using FMM")
    print("n - inpaint using NS technique")
    print("r - reset the inpainting mask")
    print("ESC - exit")

    # Read image in color mode.
    # img = cv2.imread(sys.argv[1], cv2.IMREAD_COLOR)
    img = cv2.imread('img1.jpg', cv2.IMREAD_COLOR)

    # If image is not read properly, return error.
    if img is None:
        print('Failed to load image file: {}'.format(args["image"]))
        return

    # Create a copy of original image.
    img_mask = img.copy()
    # Create a black copy of original image, acts as a mask.
    inpaintMask = np.zeros(img.shape[:2], np.uint8)
    # Create sketch using OpenCV Utility Class: Sketcher.
    sketch = Sketcher('image', [img_mask, inpaintMask], lambda: ((255, 255, 255), 255))

    while True:
        ch = cv2.waitKey()
        if ch == 27:
            break
        if ch == ord('t'):
            # Use Algorithm proposed by Alexendra Telea: Fast Marching Method (2004)
            res = cv2.inpaint(
                src=img_mask, inpaintMask=inpaintMask, inpaintRadius=3, flags=cv2.INPAINT_TELEA)
            cv2.imshow('Inpaint Output using FMM', res)
        if ch == ord('n'):
            # Navier-Stokes, Fluid Dynamics, and Image and Video Inpainting (2001).
            res = cv2.inpaint(
                src=img_mask, inpaintMask=inpaintMask, inpaintRadius=3, flags=cv2.INPAINT_NS)
            cv2.imshow('Inpaint Output using NS Technique', res)
        if ch == ord('r'):
            img_mask[:] = img
            inpaintMask[:] = 0
            sketch.show()

    print('Completed')


if __name__ == '__main__':
    main()
    cv2.destroyAllWindows()
