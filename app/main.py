import logging
import os
import random

import cv2
import numpy as np
import pygame
from make87 import initialize, get_publisher
from make87_messages.core.header_pb2 import Header
from make87_messages.image.compressed.image_jpeg_pb2 import ImageJPEG


def main():
    initialize()
    topic = get_publisher(name="SCREEN_CAPTURE", message_type=ImageJPEG)

    def encode_to_jpeg(frame: np.ndarray) -> np.ndarray:
        _, encoded_image = cv2.imencode(".jpeg", frame)
        return encoded_image

    def publish_frame(frame: np.ndarray):
        jpeg = encode_to_jpeg(frame=frame)

        header = Header()
        header.timestamp.GetCurrentTime()
        message = ImageJPEG(header=header, data=jpeg.tobytes())
        topic.publish(message)
        logging.info(f"Published logo frame with size {len(jpeg)} bytes")

    # Initialize Pygame
    pygame.init()

    # Set screen size to 1920x1080
    screen_width, screen_height = 1920, 1080
    screen = pygame.display.set_mode((screen_width, screen_height))

    # Set up colors
    BLACK = (0, 0, 0)
    DVD_COLOR = [random.randint(50, 255), random.randint(50, 255), random.randint(50, 255)]

    # Set up DVD logo properties
    logo_width, logo_height = 120, 60
    logo_x = random.randint(0, screen_width - logo_width)
    logo_y = random.randint(0, screen_height - logo_height)
    logo_speed_x = 3
    logo_speed_y = 3

    # Load or create a DVD logo with a larger font size
    font_size = 96  # Larger font size for 1920x1080 resolution
    font = pygame.font.SysFont("Arial", font_size, bold=True)
    logo_text = font.render("make87", True, DVD_COLOR)

    # Function to change color when bouncing
    def change_color():
        return [random.randint(50, 255), random.randint(50, 255), random.randint(50, 255)]

    # Game loop
    running = True
    clock = pygame.time.Clock()

    while running:
        screen.fill(BLACK)

        # Move the logo
        logo_x += logo_speed_x
        logo_y += logo_speed_y

        # Bounce on the edges and change color
        if logo_x <= 0 or logo_x >= screen_width - logo_width:
            logo_speed_x *= -1
            DVD_COLOR = change_color()
            logo_text = font.render("make87", True, DVD_COLOR)
        if logo_y <= 0 or logo_y >= screen_height - logo_height:
            logo_speed_y *= -1
            DVD_COLOR = change_color()
            logo_text = font.render("make87", True, DVD_COLOR)

        # Draw the logo
        screen.blit(logo_text, (logo_x, logo_y))

        # Capture the frame into memory (with correct shape)
        frame_data = pygame.surfarray.array3d(screen)

        # Transpose frame_data to have (height, width, 3) instead of (width, height, 3)
        frame_data = np.transpose(frame_data, (1, 0, 2))  # Swap axes to get correct shape

        # Publish the frame as JPEG
        publish_frame(frame=frame_data)

        # Update the screen
        pygame.display.flip()

        # Cap the frame rate
        clock.tick(60)

        # Handle events
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

    # Quit Pygame
    pygame.quit()


if __name__ == "__main__":
    # Set the environment variable to use the dummy video driver (for headless mode)
    os.environ["SDL_VIDEODRIVER"] = "dummy"
    main()
