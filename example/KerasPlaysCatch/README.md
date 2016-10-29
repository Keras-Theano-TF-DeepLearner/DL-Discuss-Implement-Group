Code for [Keras plays catch](http://edersantana.github.io/articles/keras_rl/) blog post

### Train
```bash
python qlearn.py
```

### Generate figures
```bash
python test.py
```

### Make gif
```bash
ffmpeg -i %03d.png output.gif -vf fps=1
```

### Requirements
* Prior supervised learning and Keras knowledge
* Python science stack (numpy, scipy, matplotlib) - Install Anaconda!
* Theano or Tensorflow
* Keras
* ffmpeg (optional)
