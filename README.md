# Spresense Facemask Detector

<p align="center">
<img src="https://i.ibb.co/fFSZyht/image-1.png" width="50%">
</p>

Spresense-based system that monitors facemask use through EdgeImpulse.

# Introduction:

Covid-19 has impacted the world like very few pandemics throughout human history. Although it has not been as lethal as other pandemics in terms of mortality, we have already had about [6,400,000](https://coronavirus.jhu .edu/map.html) lethal cases according to Johns Hopkins University (01-08-2022).

Although much of the world's population has already been vaccinated, throughout these 3 years the virus has had mutations, which according to the [WHO](https://www.who.int/data/gho/publications/world- health-statistics) is still valid as of today (01-08-2022).

<img src="https://i.ibb.co/tXdDZMw/image.png">

Due to this, the use of face masks, even if they already have the vaccines, continues to be essential for the public health of most countries. 

# Solution:

We created a system based on Sony's Spresense board which, thanks to its camera and the Edge Impulse framework, we are able to create a reliable and simple mask detection system for the entrance of a home.

# Connection Diagram:

## Backend Diagram:

<img src="https://i.ibb.co/cgSPHJ4/Scheme-drawio.png">

## Hardware:

<img src="https://i.ibb.co/jJgm40s/Image.png">

# Edge Impulse:

We used Edge Impulse as the development platform for all the software in Sony's Spresense, this in order to quickly develop a neural network that would work with the Spresense and we could obtain a functional and efficient product.

<img src="https://i.ibb.co/9Y5tffj/image.png">

Edge Impulse Link: 

Do not forget to configure the Edge Impulse CLI to be able to debug the device.

https://docs.edgeimpulse.com/docs/edge-impulse-cli/cli-overview

## Dataset:

For this problem of performing a facemask detector, it was first necessary to have a dataset with 3 types of basic detections, face detection with a face mask, face detection without a face mask, and null detection when there is no face in front of the camera.

<img src="https://i.ibb.co/Qpc08pZ/check.png">

The entire dataset will be in the edge impulse project.

## Impulse Design:

The correct design of the Impulse is very important since this will affect the efficiency of our neural network and even if it will be compatible with the hardware.

For our Impulse it was decided to keep the images 96x96x3 (contemplating that the third dimension of the tensor are the 3 RGB channels of the images) since it is one of the resolutions that our camera supports and in turn will allow us fast results.

<img src="https://i.ibb.co/r0DPqvq/image.png">

We invite you to try more combinations of our dataset to obtain better results!

## Training:

For the training of the neural network the following hyperparameters were used.

<img src="https://i.ibb.co/XXVqjCY/image.png">

MobileNetV2 96x96 0.1 was used, which allowed us a model with only 212.7K flash weight and an inference time of 108ms. More than enough for our project.

<img src="https://i.ibb.co/10MYgCn/image.png">

Finally, the confusion matrix of our project gave us the following results.

<img src="https://i.ibb.co/w77RkTM/image.png">

## Model testing:

95% accuracy sounds great, but now let's look at the results of our neural network against the testing data.

<img src="https://i.ibb.co/YQr8jHq/image.png">

With the neural network validated with the test data, we could be more sure that it would be the ideal one for our device, now it's time to take it to our device.

## Build and Flash:

In this section we will select the hardware that we are going to use to deploy our neural network, in this case spresense is fully capable of deploying the model.

<img src="https://i.ibb.co/4dNhk0d/image.png">

For the Optimizations part, the EON compiler comes by default, in my opinion always leave it activated to display the model, but we leave it to the discretion of the reader.

<img src="https://i.ibb.co/dmxckJG/image.png">

Finally, by clicking on Build, we will download a folder with everything necessary to flash on our device.

<img src="https://i.ibb.co/F0tcbHt/image.png">

Being executable files, we will only have to run the program according to the operating system we have.

## Testing:

Once we flash the binary on our device, we can run the following command in our terminal.

    edge-impulse-run-impulse --debug

<img src="https://i.ibb.co/br72J2t/image.png">

It could vary depending on the PC, but in our case, once this code has been executed, we will be able to see the images and predictions of our device in real time in any browser.

http://172.25.176.1:4915/

Here is a sample of how we can see the images.

Negative Detection:

<img src="https://i.ibb.co/Q6VBjKv/image.png">

Facemask ON:

<img src="https://i.ibb.co/2cY1jD3/image.png">

Facemask OFF:

<img src="https://i.ibb.co/mvLb9B5/image.png">

# Raspberry-Pi Gateway:

As we could see, our model was a complete success and we were able to detect the negatives and the facemask without any problem.

Now in order to be able to put our device on our driveway and run Impulse, we use a raspberry pi to be able to send all the data from it to the cloud, so the first thing to do is to have a raspberry pi with edge impulse installed.

<img src="https://i.ibb.co/61JZZYD/image.png">

## AWS:

Now that we have the correct software, we also have to have a place to send the data, in this case for personal taste we prefer to use AWS IoT to send all the data to the cloud in a simple way.

### AWS IoT:

In this case we must have AWS IoT access, however the only consideration that must be taken is the region. For our case us-west-1.

<img src="https://i.ibb.co/gz6cqkT/image.png">

### AWS Lambda:

In order to send data to AWS IoT as if we were a device, we will use a lambda function.

<img src="https://i.ibb.co/N7fcKX2/image.png">

The lambda function is already in the [Lambda](./Lambda/lambda_function.py) folder.

### AWS IAM:

We also have to give the Lambda permissions to access the AWS IoT resources, so in the IAM services we will configure the permissions for the lambda.

<img src="https://i.ibb.co/7tmX0Px/image.png">

### API Gateway:

Now as the final phase of the process, we must create an API with which we can access and send the data from our website to AWS.

<img src="https://i.ibb.co/ZK1SvH1/image.png">

## Edge Impulse Cli Soft Hack:

To take advantage of the software that EdgeImpulse already gives us, we will have to go to the JS file that the website uses to give us the data.

In the case of the raspberry pi it would be the following path.

    /usr/local/lib/node_modules/edge-impulse-cli/build/public/camera-live-view.js

We first alter the connect event to notify the AWS console that a device is connected.

    socket.on('connect', () => {
            var config = {
                method: 'get',
                url: 'https://xxxxxxxxxx.execute-api.us-east-1.amazonaws.com/General-IoT-Device',
                headers: {
                    "device": "spres",
                    "topic": "connect",
                    "data": "OK"
                }
            };
            axios(config)
                .then(function (response) {
                    console.log(JSON.stringify(response.data));
                })
                .catch(function (error) {
                    console.log(error);
                });
            socket.emit('hello');
        });

In the second modification, we are going to send all the results to AWS IoT from our API.

    socket.on('classification', (opts) => {
        let result = opts.result;
        els.timePerInference.textContent = opts.timeMs;
        axios({
            method: 'get',
            url: 'https://xxxxxxxxxx.execute-api.us-east-1.amazonaws.com/General-IoT-Device',
            headers: {
                "device": "spres",
                "topic": "result",
                "data": JSON.stringify(result.classification)
            }
        })
            .then(function (response) {
                console.log("AWS IoT OK");
            })
            .catch(function (error) {
                console.log(error);
            });

Of course, this cannot be limited to AWS IoT, you can modify the API Call to send the data to any other site, just by changing the URL.

# Mini DEMOS:

Facemask Detection:

[![Image](https://i.ibb.co/fFSZyht/image-1.png)](https://youtu.be/nqbx9q1HxZU)

AWS IoT:

[![Image](https://i.ibb.co/fFSZyht/image-1.png)](https://youtu.be/Uoa5IXYL2Cs)

# Final Product:

Case open:

<img src="https://i.ibb.co/hyXG8mM/1.png" height="270px"><img src="https://i.ibb.co/TkPV8Bj/20220727-003455.png" height="270px">

Case closed:

<img src="https://i.ibb.co/0MRNMWt/20220727-003336.png" height="270px"><img src="https://i.ibb.co/L0mLFXv/20220727-003341.png" height="270px">

# DEMO:

[![Image](https://i.ibb.co/fFSZyht/image-1.png)](PENDING!)

Thanks for reading!
