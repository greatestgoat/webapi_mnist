from keras.applications import ResNet50
from tensorflow.keras.models import load_model
from keras.preprocessing.image import img_to_array
from keras.applications import imagenet_utils
from PIL import Image
import numpy as np
import flask
import io

# initialize our Flask application and the Keras model
app = flask.Flask(__name__)
model = None

def load_models():
    # load the pre-trained Keras model (here we are using a model
    # pre-trained on ImageNet and provided by Keras, but you can
    # substitute in your own networks just as easily)
    global model
    # model = ResNet50(weights="imagenet")
    model = load_model('./mnist_models.h5')

def prepare_image(image, target):
    # if the image mode is not RGB, convert it
    # if image.mode != "RGB":
    #     image = image.convert("RGB")

    # resize the input image and preprocess it
    image = image.resize(target)
    image = img_to_array(image)
    print(img_to_array)
    image = np.array(image)
    image = image.reshape(-1, 784)
    # image = np.expand_dims(image, axis=0)
    image = imagenet_utils.preprocess_input(image)

    # return the processed image
    return image

@app.route("/predict", methods=["POST"])
def predict():
    # initialize the data dictionary that will be returned from the
    # view
    data = {"success": False}

    # ensure an image was properly uploaded to our endpoint
    if flask.request.method == "POST":
        if flask.request.files.get("image"):
            # read the image in PIL format
            image = flask.request.files["image"].read()
            image = Image.open(io.BytesIO(image))

            # preprocess the image and prepare it for classification
            image = prepare_image(image, target=(28, 28))

            # classify the input image and then initialize the list
            # of predictions to return to the client
            preds = model.predict(image)
            pred_classes = model.predict_classes(image)
            # pred_probs = preds
            results = [(pred_classes[0], np.max(preds[0]))]
            print("------------------------")
            print(pred_classes)
            print("------------------------")
            # results = imagenet_utils.decode_predictions(preds)
            data["predictions"] = []

            # loop over the results and add them to the list of
            # returned predictions
            for (classes, prob) in results:
                r = {"class": int(classes), "probability": float(prob)}
                data["predictions"].append(r)

            # indicate that the request was a success
            data["success"] = True

    # return the data dictionary as a JSON response
    return flask.jsonify(data)

if __name__ == "__main__":
	print(("* Loading Keras model and Flask starting server..."
		"please wait until server has fully started"))
	load_models()
	# app.run()
	app.run(debug = False, threaded = False)