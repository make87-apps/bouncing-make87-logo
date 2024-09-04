# bouncing-make87-logo

This application creates a dynamic animation of the "make87" logo that moves around a 1920x1080 window, bouncing off the
edges and changing color on each bounce. The application is designed to demonstrate how real-time visual data can be
captured, processed, and transmitted.

## Overview

The app runs a graphical window using Pygame, where the "make87" logo moves across the screen. The logo's position is
updated continuously, and when it reaches the edge of the screen, it reverses direction and takes on a new random color.
This creates a dynamic, continuously changing visual effect.

## Frame Capture and Processing

While the logo moves and bounces, each frame of the animation is captured directly from the screen. The frame data,
which consists of the current visual content, is then processed as follows:

1. **Frame Capture**: The current screen content is captured as an array of pixel data. This data represents the color
   and position of every element visible in the window at a given time.

2. **JPEG Encoding**: Each captured frame is encoded into JPEG format using OpenCV, which compresses the image data into
   a more efficient format for transmission or storage.

3. **Message Publishing**: The JPEG-encoded frame is then published through a message-passing system. This demonstrates
   how graphical data can be packaged and transmitted as soon as they have been captured, allowing it to be consumed by
   other systems or
   services.

## Application Logic

- **Pygame for Rendering**: The graphical interface is handled by Pygame, which manages the window, screen rendering,
  and event handling. The position and velocity of the "make87" logo are updated in each iteration of the main game
  loop.

- **Color and Bounce Behavior**: The logo's color is randomly generated and changes each time the logo bounces off the
  edge of the window. This color update, along with the movement, is continuously processed, giving the appearance of an
  active, bouncing object.

- **Publishing Frames**: After updating the logo’s position and rendering the frame, the frame is captured, converted to
  the correct data format, and published to a specified topic using the message framework provided by the `make87`
  library. The frame rate is capped to ensure smooth performance.

This structure demonstrates how graphical elements can be captured, processed, and transmitted in real-time, offering
insight into building similar real-time streaming or capture applications.

## Demo

![Animation of Logo](https://github.com/make87/bouncing-make87-logo/blob/assets/make87-bouncing.gif)