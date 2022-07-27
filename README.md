# Spresense-Facemask-Detector

<img src="https://i.ibb.co/WvztyFN/image.png" width="50%">

Spresense-based system that monitors facemask use through EdgeImpulse.

# Introduction:

El Covid-19, ha impactado al mundo como muy pocas pandemias a lo largo de la historia humana, que no ha sido tan letal como otras pandemias en grado de mortalidad ya hemos tenido cerca de [6,400,000](https://coronavirus.jhu.edu/map.html) segun la universidad de Johns Hopkins (08-01-2022).

Aunque ya ha sido vacunada mucha de la poblacion mundial, a lo largo de estos 3 años el virus ha tenido mutaciones, las cuales segun la [WHO](https://www.who.int/data/gho/publications/world-health-statistics) aun sigue vigente al dia de hoy (08-01-2022).

<img src="https://i.ibb.co/tXdDZMw/image.png">

Debido a esto, el uso de cubrebocas, aun se tengan ya las vacunas, sigue siendo indispensable para la salud publica de cada pais.

# Solution:

Creamos un sistema basado en la Sony's Spresense board el cual gracias a su camara y el framework de Edge Impulse, somos capaces de crear un sistema de deteccion de cubrebocas para la entrada de un hogar, fiable y sencillo.

# Connection Diagram:

## Backend Diagram:

<img src="https://i.ibb.co/cgSPHJ4/Scheme-drawio.png">

## Hardware:

<img src="https://i.ibb.co/jJgm40s/Image.png">

# Edge Impulse:

Usamos Edge Impulse como development platform para todo el software en la ​Sony's Spresense, esto con el fin de rapidamente poder desarrollar una red neuronal que funcionara con la Spresense y pudieramos obtener un producto funcional y eficiente.

<img src="https://i.ibb.co/9Y5tffj/image.png">

Edge Impulse Link: 

No olvides configurar la Edge Impulse CLI para poder hacer el Debug del device.

https://docs.edgeimpulse.com/docs/edge-impulse-cli/cli-overview

## Dataset:

Para este problema de realizar un facemask detector primero fue necesario tener un dataset con 3 tipos de detecciones basicas, deteccion de cara con cubrebocas, deteccion de cara sin cubrebocas y deteccion nula cuando no hay un rostro frente a la camara.

<img src="https://i.ibb.co/Qpc08pZ/check.png">

NOTA: Todo el dataset estara en el proyecto de edge impulse.

## Impulse Design:

El diseño correcto del Impulse es muy importante ya que esto repercutira en la eficiencia e nuestra red neuronal e incluso si sera compatible con el hardware.

Para nuestro Impulse se decidio mantener las imagenes 96x96x3 (contemplando que esa tercera dimension del tensor son los 3 canales de RGB de las imagenes) ya que es una de las resoluciones que aguanta nuestra camara y a su vez nos permitira resultados rapidos.

<img src="https://i.ibb.co/r0DPqvq/image.png">

NOTA: Te invitamos a probar mas combinaciones de nuestro dataset para obtener mejores resultados!

## Training:

Para el entrenamiento de la red neuronal se usaron los siguientes hiperparametros.

<img src="https://i.ibb.co/XXVqjCY/image.png">

Se utilizo MobileNetV2 96x96 0.1, lo cual nos permitio un modelo de solo 212.7K de peso en flash y un tiempo de inferencia de 108ms. mas que suficiente para nuestro proyecto.

<img src="https://i.ibb.co/10MYgCn/image.png">

Finalmente la matriz de confusion de nuestro proyecto nos dio los siguientes resultados.

<img src="https://i.ibb.co/w77RkTM/image.png">

## Model testing:

Suena muy bien un 95% de presicion, pero ahora veamos los resultados de nuestra red neuronal contra la testing data.

<img src="https://i.ibb.co/YQr8jHq/image.png">

Ya con la red neuronal validada con los datos de prueba, pudimos estar mas seguros de que seria la ideal para nuestro device, ahora llego la hora de llevarla a nuestro device.

## Build and Flash:

En esta seccion seleccionaremos el Hardware que vamos a utilizar para desplegar nuetra red neuronal, en este caso la spresense es completamente capaz de desplegar el modelo.

<img src="https://i.ibb.co/4dNhk0d/image.png">

Para la parte de Optimizations ya viene por defecto el EON compiler, en mi opinion siempre dejalo activado para desplegar el modelo, pero lo dejamos a la discrecion del lector.

<img src="https://i.ibb.co/dmxckJG/image.png">

Por ultimo al hacer clic en Build nos descargara un folder con todo lo necesario para realizar el flash en nuestro device.

<img src="https://i.ibb.co/F0tcbHt/image.png">

Al ser archivos ejecutables, solo tendremos que ejecutar el programa segun el sistema operativo que tengamos.

## Testing:

Una vez realizamos el flash del binario en nuestro device, podremos correr el siguiente comando en nuestra terminal.

    edge-impulse-run-impulse --debug

<img src="https://i.ibb.co/br72J2t/image.png">

Podria llegar a variar segun la pc, pero en nuestro caso una vez ejecutado este codigo podremos ver en cualquier navegador las imaganes y predicciones de nuetro device en tiempo real.

http://172.25.176.1:4915/

Aqui una muestra del como podemos ver las imagenes.

Negative Detection:

<img src="https://i.ibb.co/Q6VBjKv/image.png">

Facemask ON:

<img src="https://i.ibb.co/2cY1jD3/image.png">

Facemask OFF:

<img src="https://i.ibb.co/mvLb9B5/image.png">

# Raspberry-Pi Gateway:

Como pudimos ver nuestro modelo fue todo un exito y pudimos sin problema detectar los negativos y la facemask.

Ahora con el fin de poder poner nuestro device en nuestra entrada y a su vez correr el Impulse, utilizamos una raspberry pi para poder mandar todos los datos desde esta a la nube, asi que lo primero sera tener una raspberry pi con edge impulse instalado.

<img src="https://i.ibb.co/61JZZYD/image.png">

## AWS:

Ahora ya que tenemos el software correcto, tenemos que ademas tener a donde mandar los datos, en este caso por gusto personal preferimos utlilizar AWS IoT para mandar todos los datos a la nube de forma sencilla.

### AWS IoT:

En este caso deberemos tener acceso AWS IoT, sin embargo la unica consideracion que hay que tener es la region. Para nuestro caso us-west-1.

<img src="https://i.ibb.co/gz6cqkT/image.png">

### AWS Lambda:

Para poder mandar datos a AWS IoT como si fueramos un device, usaremos una funcion lambda.

<img src="https://i.ibb.co/N7fcKX2/image.png">

Ya la funcion lambda esta en la carpeta [Lambda](./Lambda/lambda_function.py).

### AWS IAM:

Tenemos ademas que darle permisos a la Lambda para acceder a los recursos de AWS IoT, entonces en el servicios de IAM confifuraremos los permisos para la lambda.

<img src="https://i.ibb.co/7tmX0Px/image.png">

### API Gateway:

Ahora como fase final del proceso, deberemos crear una API con la cual podamos acceder y mandar los datos desde nuestra pagina web a AWS.

<img src="https://i.ibb.co/ZK1SvH1/image.png">

## Edge Impulse Cli Soft Hack:

En este caso para aprovechar el software que ya nos da EdgeImpulse tendremos que ir al archivo JS que utiliza la pagina web para darnos los datos.

En el caso de la raspberry pi seria el siguiente path.

    /usr/local/lib/node_modules/edge-impulse-cli/build/public/camera-live-view.js

Primero alteramos el evento de connect para avisar a la consola de AWS que hay un device conectado.

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

En la segunda modificacion, vamos a mandar todos los resultados a AWS IoT desde nuestra API.

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

Claro que esto no se puede quedar en solo AWS IoT puedes modificar la API Call para mandar los datos a cualquier otro sitio, solo cambiando la URL.

# Mini DEMOS:

Facemask Detection:

[![Image](https://i.ibb.co/WvztyFN/image.png)](PENDING!)

# Final Product:

Case open:

<img src="https://i.ibb.co/hyXG8mM/1.png" height="270px"><img src="https://i.ibb.co/TkPV8Bj/20220727-003455.png" height="270px">

Case close:

<img src="https://i.ibb.co/0MRNMWt/20220727-003336.png" height="270px"><img src="https://i.ibb.co/L0mLFXv/20220727-003341.png" height="270px">

# EPIC DEMO:

[![Image](https://i.ibb.co/WvztyFN/image.png)](PENDING!)

Thanks for reading!