# Language Flashcard Generator

## Learn vocabulary in new language fast have fun doing it

This script generates printable pdf with flashcards for learning languages. Learn vocabulary with physical aids and minimal effort.

You just need to run command similar to following:
```sh
python lfc_generator.py --target_language it --source_language en --rows 6 \ --cols 4 --word_count 2500
```

![image](https://user-images.githubusercontent.com/45427816/214693411-9649746d-ae3d-4e71-a3aa-6f51a8beb6a8.png)

Unfortunately, you have to cut them yourself ✂️😊. You can set how many cards you need fit to one page base on your needs. You can change following variables using the command line parameters:
- `-t` or `--target_language`: Language you are going to learn. Any language supported by google translate is supported. however, I cannot guarantee the quality of the translation, as it is done by a robot. To learn available codes go to https://developers.google.com/admin-sdk/directory/v1/languages
  - Example: `-t fr`
  - Default: `--target_language en`
- `-s` or `--source_language`: Language you know, file \lemmas\lemmas_<lang_code>.txt is expected. You can create the file manually if you have certain words you wanna learn in mind or you can use/edit lemmas provided fo "cs" or "en" languages. They contain most used words in both provided languages.
    - Example: `-s en`
    - Default: `--source_language cs`
- `-r` or `--rows`: Number of rows on one page. 6 is recommended to have card about 5cm or 2 inches in height.
    - Example: `-r 4`
    - Default: `--rows 6`
- `-c` or `--cols`: Number of columns on one page. 4 is recommended to have card about 5cm or 2 inches in height.
    - Example: `-c 3`
    - Default: `--cols 4`
- `-w` or `--word_count`: Number of words to be generated. To not waste paper, number of words will be rounded up to fully cover all pages.
    - Example: `-w 2000`
    - Default: `--word_count 250`
## TODO:
- Functionality for custom fonts.
- Provide lemma corpus in additional languages.
- Executable file for various platforms.
