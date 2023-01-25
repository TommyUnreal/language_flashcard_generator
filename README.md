# Language Flashcard Generator

## Learn vocabulary in new language fast have fun doing it

This script generates printable pdf with flashcards for learning languages. Learn vocabulary with physical aids and minimal effort.

![image](https://user-images.githubusercontent.com/45427816/214693411-9649746d-ae3d-4e71-a3aa-6f51a8beb6a8.png)

Unfortunately, you have to cut them yourself ✂️😊. You can set how many cards you need fit to one page base on your needs. Just navigate to main part of script na change following variables:

- `target_language`: Language you are going to learn. Any language supported by google translate is supported. however, I cannot guarantee the quality of the translation, as it is done by a robot. To learn available codes go to https://developers.google.com/admin-sdk/directory/v1/languages
- `source_language`: Language you know, file \lemmas\lemmas_<lang_code>.txt is expected. You can create the file manually if you have certain words you wanna learn in mind or you can use/edit lemmas provided fo "cs" or "en" languages. They contain most used words in both provided languages.
- `rows`: Number of rows on one page. 6 is recommended to have card about 5cm or 2 inches in height.
- `cols`: Number of columns on one page. 4 is recommended to have card about 5cm or 2 inches in height.
- `size`: Number of words to be generated. To not waste paper, number of words will be rounded up to fully cover all pages.

## TODO:
- Configuration should be available via command line parameters.
- Functionality for custom fonts.
- Provide lemma corpus in additional languages.
- Executable file for various platforms.
