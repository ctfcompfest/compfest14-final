# COMPFEST-Bin

Sui

---

## Flag

```
COMPFEST14{bl3ssing_1n_disguise_s0m3times_f3lt_p4inful_than_1_thought_1111689eab}
```

## Description
>Another faulty clone webservice. But, I guess there's something special beneath it

```
http://<ip>:12021
```

## Difficulty
Tingkat kesulitan soal: medium/hard (?)

## Hints
* Due to its improper input validation & deprecated dependency, I guess someone might be able to leak the source code

## Tags
lfi, sqli, weasyprint

## Deployment
**Build & run the container**
```bash
$ docker-compose  up -d --build
```

**Stop the container**
```bash
$ docker-compose down
```

**Monitoring the container logs**
```bash
$ docker-compose logs

# or use ctop instead
# https://github.com/bcicen/ctop
$ ctop
```

## Notes
intentionally left empty

