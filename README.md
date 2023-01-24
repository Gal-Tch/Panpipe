# Panpipe

## About
This project allows creating stl files of panpipes tailored to custom needs.
The user can specify how many flutes should the panpipe have, the frequency of each flute and the width.


## CLI example
* Please make sure that your current working directory is the project root.
* This project is tested on Blender 2.93.5. 

Simple example to create two flutes of lengths 140 and 190 (sorted):
```
blender -b flute_with_full_faces.blend -P panpipe_entrypoint.py -- --freqs 140  190.5
```


Example to create three flutes of lengths 140, 190 and 170.4, and width of 5 mm. The flutes will be sorted:
```
blender -b flute_with_full_faces.blend -P panpipe_entrypoint.py -- --freqs 140  190 170.4 --sorted --dimensions 5
```

Example to create panpipe with 4 flutes, without sorting the flutes and saving it to file pipe.stl:
```
blender -b flute_with_full_faces.blend -P panpipe_entrypoint.py -- -f 140  190  200 220  -o pipe.stl --no-sorted -d 5
```