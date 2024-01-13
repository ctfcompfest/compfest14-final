# n0talogus

by twoface

---

## Flag

```
COMPFEST14{s33_7H3_l0g!!!!_459b516942}
```

## Objective
execute `history` command and leverage `histexpand commands` to execute command

## Description
"__*History repeats itself. Hence, it's the best teacher.*__" that's what she said.

## Difficulty
easy-medium

## Hints
expand the token and you are good to go!

## Tags
Bash, histexpand

## Deployment
Penjelasan cara menjalankan service yang dibutuhkan serta requirementsnya.

#### Contoh 1
- Install docker engine>=19.03.12 and docker-compose>=1.26.2.
- Run the container using:
    ```
    docker-compose up --build --detach
    ```

#### Contoh 2
- How to compile:
    ```
    gcc soal.c -o soal -O2 -D\_FORTIFY\_SOURCE=2 -fstack-protector-all -Wl,-z,now,-z,relro -Wall -no-pie
    ```
- Jalankan:
    ```
    ./soal
    ```
- Workdir di `/home/compfest14`
- Gunakan libc 2.31 ketika sudah keluar. Alias Ubuntu 20.04.

## Notes
ku masih gatau ini gimana deploymentnya
