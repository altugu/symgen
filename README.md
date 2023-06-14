## usage

```
$ make
$ ./main models/mesh<#MODEL_NUMBER>.off <#MODEL_NUMBER>_samples.txt
$ python3 main.py  models/mesh<#MODEL_NUMBER>.off input_points/<#MODEL_NUMBER>_input.txt sampled_points/<#MODEL_NUMBER>_samples.txt 
```

### sample usage
```
make
./main models/mesh023.off 23_samples.txt
python3 main.py  models/mesh023.off input_points/23_input.txt sampled_points/23_samples.txt
```
---------

#### directories

models/ : input mesh models .off format

input_points/ : manually selected two points to draw a line specific for model

sampled_points/ : evely spaced sampled points (written after cpp executable run)
