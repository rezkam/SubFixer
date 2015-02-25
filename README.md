##**SubFixer**
SubFixer does a bit of string manipulation and datetime math to shift your subtitles to match your film and decode string to unicode and fix problems with Persian.
SubFixer is based on [Ali Vakilzade](https://github.com/aliva/) SubtitleFixer and [delwin](https://github.com/enceladus/) subtitle-shifter.

###Install SubFixer
```
$ pip install subfixer
```

###Fix persian subtitles
```
$ subfixer input_file_name.srt --fix_persian
```

###Shift time
```
$ subfixer input_file_name.srt --shif 10 #shift 10 secound
```

###More help and options
```
$ subfixer --help
```

