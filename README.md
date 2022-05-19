## Using web-server Google Colab to run an application in Bioprocess Library

Google Colab is essentially a VM Ubuntu 18.04 machine that people with a google-account can get. You configure it yourself and can have 
it for up to 12 hours and then it is closed. Next time you need to configure again. It is pre-configured with Python 3.7 and some common libraries 
and you interact through a Colab notebook that is based on Jupyter notebook. More about it you can find here...

I have made a notebook that set-up PyFMI 2.7.4 and needed libraries and run a small example with microbial batch cultivation.
The model is an example taken from Bioprocess Library and the example is available as an FMU. You can interact with it through a simplified
command-line interface using: newplot(), par(), inut(), simuI() etc. More about the command-line interface you finde here...

Below a diagram with two simulations of batch growth with different initial substrate level that you will get at the end of the notebook.
