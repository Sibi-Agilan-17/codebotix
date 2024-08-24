import asyncio

import cv2

from gpiozero import Motor


"""
Motor numbers

Forward
###################
1                 2


3                 4
###################
Backward
"""


# Initialize four motors
motor1 = Motor(forward=17, backward=18)
motor2 = Motor(forward=22, backward=23)
motor3 = Motor(forward=24, backward=25)
motor4 = Motor(forward=27, backward=28)
motors = [motor1, motor2, motor3, motor4]


def capture_image(save_path: str) -> None:
    """Capture an image from the computer camera and save it to the specified path."""

    # Initialize the camera
    cap = cv2.VideoCapture(0)

    if not cap.isOpened():
        print("Error: Could not open camera.")
        return

    # Capture a single frame
    ret, frame = cap.read()

    if ret:
        # Save the captured image
        cv2.imwrite(save_path, frame)
        print(f"Image saved to {save_path}")
    else:
        print("Error: Could not capture image.")

    # Release the camera
    cap.release()
    cv2.destroyAllWindows()


async def move_robot(directions: list[int], ticks: int) -> None:
    """Move the robot in the specified direction for the given number of ticks."""
    for _ in range(ticks):
        for d, m in zip(directions, motors):
            if d == 1:
                m.forward()
            elif d == 0:
                m.stop()
            elif d == -1:
                m.backward()
        await asyncio.sleep(0.1)


async def move_forward(ticks: int) -> None:
    """Move the robot forward."""
    return await move_robot([1, 1, 1, 1], ticks)


async def move_backward(ticks: int) -> None:
    """Move the robot backward."""
    return await move_robot([-1, -1, -1, -1], ticks)


async def move_left(ticks: int) -> None:
    """Move the robot left."""
    return await move_robot([-1, 1, -1, 1], ticks)


async def move_right(ticks: int) -> None:
    """Move the robot right."""
    return await move_robot([1, -1, 1, -1], ticks)


async def stop() -> None:
    """Stop the robot."""
    for m in motors:
        m.stop()

