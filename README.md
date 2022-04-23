# SubFixer
SubFixer does a bit of string manipulation and datetime math to shift your subtitles to match your film and decode string to unicode and fix problems with Persian.
SubFixer is based on [Ali Vakilzade](https://github.com/aliva/) SubtitleFixer and [delwin](https://github.com/enceladus/) subtitle-shifter.

## Install SubFixer
```
$ pip install subfixer
```

## Usage

Simple fix subtitles:

```shell
$ subfixer input.srt
```

Shifting some second times:
```shell
$ subfixer input.srt --shif 10    # Shift 10 secound
```

for more help and options:
```shell
$ subfixer --help
```

