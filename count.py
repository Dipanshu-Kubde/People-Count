import cv2
import imutils
import numpy as np
import argparse


# Define HOGCV outside of any function
HOGCV = cv2.HOGDescriptor()
HOGCV.setSVMDetector(cv2.HOGDescriptor_getDefaultPeopleDetector())

def detect(frame, confidence_threshold=0.5):
    bounding_box_cordinates, weights = HOGCV.detectMultiScale(frame, winStride=(4, 4), padding=(8, 8), scale=1.03)

    person = 1
    for x, y, w, h in bounding_box_cordinates:
        confidence = weights[0][person - 1]
        if confidence > confidence_threshold:
            cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)
            cv2.putText(frame, 'person: {} ({:.2f})'.format(person, confidence), (x, y), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 255), 1)
            person += 1
    cv2.putText(frame, 'Status: Detecting', (40, 40), cv2.FONT_HERSHEY_DUPLEX, 0.8, (255, 0, 0), 2)
    cv2.putText(frame, 'Total Persons: {}'.format(person), (40, 70), cv2.FONT_HERSHEY_DUPLEX, 0.8, (255, 0, 0), 2)
    cv2.imshow('output', frame)

    return frame


def detectByPathImage(path, output_path, confidence_threshold=0.5):  # Added confidence_threshold parameter
    image = cv2.imread(path)

    image = imutils.resize(image, width=min(800, image.shape[1]))

    result_image = detect(image, confidence_threshold)  # Pass the confidence_threshold to detect function

    if output_path is not None:
        cv2.imwrite(output_path, result_image)

    cv2.waitKey(0)
    cv2.destroyAllWindows()

def humanDetector(args):
    image_path = args["image"]
    video_path = args['video']
    if str(args["camera"]) == 'true': 
        camera = True
    else: 
        camera = False

    writer = None
    if args['output'] is not None and image_path is None:
        writer = cv2.VideoWriter(args['output'], cv2.VideoWriter_fourcc(*'MJPG'), 10, (600, 600))

    if camera:
        print('[INFO] Opening Web Cam.')
        detectByCamera(args['output'], writer)
    elif video_path is not None:
        print('[INFO] Opening Video from path.')
        detectByPathVideo(video_path, writer)
    elif image_path is not None:
        print('[INFO] Opening Image from path.')
        detectByPathImage(image_path, args['output'])

def argsParser():
    arg_parse = argparse.ArgumentParser()
    arg_parse.add_argument("-i", "--image", default=None, help="Path to input image")
    arg_parse.add_argument("-v", "--video", default=None, help="Path to input video")
    arg_parse.add_argument("-c", "--camera", default=False, help="Set to 'true' to use the camera")
    arg_parse.add_argument("-o", "--output", default=None, help="Path to output image or video")
    args = vars(arg_parse.parse_args())
    return args


if __name__ == "__main__":
    HOGCV = cv2.HOGDescriptor()
    HOGCV.setSVMDetector(cv2.HOGDescriptor_getDefaultPeopleDetector())
    
    args = argsParser()  # Parse command-line arguments
    if args["image"] is not None:
        image = cv2.imread(args["image"])  # Load the image
        detectByPathImage(args["image"], args["output"])
    else:
        print("No image specified. Please specify an image with the -i option.")
    humanDetector(args)   # Call the humanDetector function with parsed arguments
