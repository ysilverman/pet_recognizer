# Pet Recognizer

This repository demonstrates an example of how to 
1. teach a resnet50 based network to recognize pets (cats and dogs) 
2. set up a backend service that can predict cat and dog images 
3. implement a CLI that talks with our backend

## Project documentation
### design document
### run instructions (env, commands)
**Model.** To teach the model, you can run the runbook https://github.com/ysilverman/pet_recognizer/blob/main/model_training/pet_recognizer.ipynb step by step. Make sure to provide access
to the dataset. By default, the notebook expects to find the dataset under the following path `/content/drive/MyDrive/Colab\ Notebooks/dogs-vs-cats-redux-kernels-edition.zip`.
The easiest way is to upload the dataset to your Drive account and then mount it in the notebook. Once the model is trained, the notebook saves it under the name `full_model`.
You can download this model if you want to use it in your development. For the purposes of the task, the trained model was added to the repo and it resides here: 
https://github.com/ysilverman/pet_recognizer/blob/main/backend/full_model

**Backend.** Run the backend with a flask command `FLASK_APP = "main" flask run` from the `backend` directory or simply run the provided docker-compose file from the root `docker-compose up -d `. 
The service will be running on port `5000`.  It has only one endpoint `POST /predict` that expects a binary file named `file` and responds with a simple json in the 
following format
```
{
    "message": "<pet>"
}
```


**Client.** The client is located here https://github.com/ysilverman/pet_recognizer/tree/main/client and uses the following semantic `python ./recognize_pet.py <image_path>`. 
The image should have 3 channels. Examples:
```
$ python .\recognize_pet.py ../samples/cat_1.jpg
cat

$ python .\recognize_pet.py ../samples/dog_1.jpg
cdog
```

### architecture, losses, metrics

The model is based on pretrained resnet50. The last layer was changed to categorize images into 2 classes. I used CrossEntropyLoss for the loss function and optim.Adam with learning rate 0.001 for the optimizer. The training was run through 10 epochs and the best model was obtained on epoch 6 with Training Loss: 0.158518 and Validation Loss: 0.048516.

## Data set

I used the [Dogs vs. Cats Redux: Kernels Edition](https://www.kaggle.com/c/dogs-vs-cats-redux-kernels-edition/data?select=sample_submission.csv) dataset. The dataset contains 25000 images of cats and dogs. I had to prepare the dataset because the provided hierarchy was invalid for the torchvision.dataset framework. The dataset was split into train:valid:test with the ratio 80%:10%:10%. The dataset was also expanded with transformers (see the code).

## Model training code
### Jupyter Notebook
https://github.com/ysilverman/pet_recognizer/blob/main/model_training/pet_recognizer.ipynb
### MLFlow project
N/A

## Service deployment and usage instructions
### dockerfile or docker-compose file

The backend was packed into a docker image and can be downloaded from [here](https://hub.docker.com/repository/docker/katya3113167/cat-dog-predictor). The image is based on `pytorch/pytorch`. The backend works synchronously.

The repo also provides a simple `docker-compose` file that launches a single backend container with exposed port 5000. 

### required services: databases
N/A
### client for service
The client is implemented as a CLI python tool. The CLI simply makes a call to the backend via Requests (assuming it's hosted on port 5000) and sends a provided image. The result of the call is displayed in the terminal

### model 
The model is a transfer learnings model based on resnet50.
