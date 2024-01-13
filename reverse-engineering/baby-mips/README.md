# baby mips?

by ReeyaDono

---

## Flag

```
COMPFEST14{m1ps_i3_e4sy_r1gHt???_b868937a70}
```

## Description
My avr challenge was so bad, so I decided to make a mips challenge, which is also very bad. This program can’t even run properly for some reason lmao. But my friend can magically run the program and give the output to me. Can you figure out what input did my friend give to the program? btw I use musl.cc.

## Difficulty
Tingkat kesulitan soal: medium

## Hints
* https://dev.to/omaremaradev/guide-to-writing-compiling-and-running-mips-binaries-on-linux-55n1
* puVar2 is pointed to the first instruction of main function

## Tags
mips, qemu-user

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
Tambahan informasi untuk soal, deployment, atau serangan yang mungkin terjadi pada service soal
