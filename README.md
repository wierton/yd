#yd

* introduction
 * A terminal bilingual dictionary by youdao API
* features
 * soundmark, definition, example sentence for English word
 * pinyin and bilingual example sentence for chinese word

### Install
	python setup.py install

### Help
```
Input[0]:
yd --help

Output[1]:
yd [options] word

-s, --save-to=[db|disk] designate the place for local cache
-u, --user=[name]       set the user to access local database
-p, --password=[passwd] set the password corresponding to the user name
-h, --help              display the help and exit
-v, --version           output version information and exit
--reset                 reset to initial state
```

### Usage
* yd --save-to=[db|disk]
 * 'db' means search history will be cached to local database
 * 'disk' means ~/.yd/.cache
* yd -u username -p password
 * directly set username and password for your database instead program ask you to fill in

### Examples
![](ex.png)

### Thanks to Flowerowl's work <https://github.com/Flowerowl/ici>
