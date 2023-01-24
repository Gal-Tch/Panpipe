# Panpipe

## About
This project allows creating stl files of panpipes tailored to custom needs.
The user can specify how many flutes should the panpipe have, the frequency of each flute and the width.


## CLI example
* Please make sure that your current working directory is the project root.
* This project is tested on Blender 2.93.5. 

Simple example to create two flutes with 500 and 400 frequencies (sorted):
```
blender -b flute_with_full_faces.blend -P panpipe_entrypoint.py -- --freqs 500  400
```


Example to create three flutes with 500, 400 and 600 frequencies, and width of 5 mm. The flutes will be sorted:
```
blender -b flute_with_full_faces.blend -P panpipe_entrypoint.py -- --freqs 500  400 600 --sorted --dimensions 5
```

Example to create the same panpipe as in previous code snippet without sorting the flutes:
```
blender -b flute_with_full_faces.blend -P panpipe_entrypoint.py -- -f 500  400  300 900 -o pipe_d5.stl --no-sorted -d 5
```