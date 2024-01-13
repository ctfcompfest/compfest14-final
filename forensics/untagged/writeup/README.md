# Untagged | Forensic (500 pts)

### **Intro**

Given a protected ZIP archive & a password. Based on its appearance and Zip extraction's status, it seems to be a normal and plain Zip-File. But upon a inspection, we got only a single file which is `INFO2` that typically used to store information of deleted files back in Windows XP era.

```bash
» 7z l untagged.zip | tail -5

2022-08-04 15:50:39 D....            0            0  Recycler/S-1-5-21-4120103722-30311560200-101401405-1002/DC1/DC2/DC4
2022-08-04 15:50:40 D....            0            0  Recycler/S-1-5-21-4120103722-30311560200-101401405-1002/DC1/DC2/DC7
2022-08-04 15:50:40 .....       157620         9017  Recycler/S-1-5-21-4120103722-30311560200-101401405-1002/INFO2
------------------- ----- ------------ ------------  ------------------------
2022-08-04 15:50:40             157620         9017  1 files, 88 folders
```

By using `rifiuti2`, we can confirm that there were some deleted files indicated by an `index`. This index then will be applied into a name convention in form of `D[drive][index].extension` that acts to store the physical content of deleted files.

```bash
» rifiuti2 INFO2 | head

Recycle bin path: 'INFO2'
Version: 5
OS Guess: Windows XP or 2003
Time zone: Coordinated Universal Time (UTC) [+0000]

Index	Deleted Time	Gone?	Size	Path
1	2022-08-04 10:59:50	No	4096	C:\flag
2	2022-08-04 10:59:50	No	4096	C:\flag\.git
3	2022-08-04 10:59:50	No	23	    C:\flag\.git\HEAD
4	2022-08-04 10:59:50	No	4096	C:\flag\.git\branches
```

Unfortunately, there's a problem. Where are those deleted files content?

### **Zip Structure Analysis**

In order to have a better understanding, lets take a close look at [Zip File specs](https://pkware.cachefly.net/webdocs/casestudies/APPNOTE.TXT)

```md
Overall .ZIP file format:

[local file header 1]
[encryption header 1]
[file data 1]
[data descriptor 1]
. 
.
.
[local file header n]
[encryption header n]
[file data n]
[data descriptor n]
[archive decryption header] 
[archive extra data record] 
[central directory header 1]
.
.
.
[central directory header n]
[zip64 end of central directory record]
[zip64 end of central directory locator] 
[end of central directory record]
```

```md
Local file header:

local file header signature     4 bytes  (0x04034b50)
version needed to extract       2 bytes
general purpose bit flag        2 bytes
compression method              2 bytes
last mod file time              2 bytes
last mod file date              2 bytes
crc-32                          4 bytes
compressed size                 4 bytes
uncompressed size               4 bytes
file name length                2 bytes
extra field length              2 bytes

file name (variable size)
extra field (variable size)
```

```md
Central directory structure:

[central directory header 1]
.
.
.
[central directory header n]
[digital signature]

File header:
    central file header signature   4 bytes (0x02014b50)
    version made by                 2 bytes
    version needed to extract       2 bytes
    general purpose bit flag        2 bytes
    compression method              2 bytes
    last mod file time              2 bytes
    last mod file date              2 bytes
    crc-32                          4 bytes
    compressed size                 4 bytes
    uncompressed size               4 bytes
    file name length                2 bytes
    extra field length              2 bytes
    file comment length             2 bytes
    disk number start               2 bytes
    internal file attributes        2 bytes
    external file attributes        4 bytes
    relative offset of local header 4 bytes

    file name (variable size)
    extra field (variable size)
    file comment (variable size)
```

Based on those schematics, we can see that a valid ZipFile basically consists of a list of `Local-Header` & `Central-Header`. For instance, `Local-Header` stores the actual property along with its data. Otherwise, `Central-Header` controls how a Zip Extractor see the catalog of files semantically.

That being said, if we happened to remove a `Central-Header` from a ZipFile, some files in the archive might not be `listed`. Thus, we can assume that was the reason why the ZipFile was detected as a valid archive despite having some abnormalities.

We can confirm the assumption by doing something simple like `string lookup`. For instance, considering an entity must have the filename appeared twicem both on `Local-Header` & `Central-Header`, then we can prove it by checking for any single occurrence of file

```bash
» strings untagged.zip | grep INFO2$
Recycler/S-1-5-21-4120103722-30311560200-101401405-1002/INFO2
Recycler/S-1-5-21-4120103722-30311560200-101401405-1002/INFO2

» strings untagged.zip | grep DC3$
Recycler/S-1-5-21-4120103722-30311560200-101401405-1002/DC1/DC2/DC3
```

Fortunately, by having some redudancies on `Local-Header` might be sufficient to craft our own `Central-Header` based on transplanted information. Using this approach, we made a [script](../src/rebuild_ch.py) to re-craft any missing `Central-Headers`.

```
» python3 rebuild_ch.py untagged.zip 

» 7z l untagged_fixed.zip | tail -5

2022-08-04 22:50:40 .....          478          289  Recycler/S-1-5-21-4120103722-30311560200-101401405-1002/DC1/DC2/DC7/DC8.sample
2022-08-04 22:50:40 .....          896          512  Recycler/S-1-5-21-4120103722-30311560200-101401405-1002/DC1/DC2/DC7/DC9.sample
2022-08-04 22:50:40 .....       157620         9017  Recycler/S-1-5-21-4120103722-30311560200-101401405-1002/INFO2
------------------- ----- ------------ ------------  ------------------------
2022-08-04 22:50:40             190195        29639  112 files, 88 folders
```

### **Recycle.Bin File Restoration**

After having ZipFile repaired, we can now get the full representation of `Recycler` directory. As discussed before, the deleted files can be restored by mapping the `filepath` info stored in `INFO2` with `D[drive][index].extension` file. Based on that approach, we made a [script](../src/info2dir.py) in order to map the `.git` directory.

```bash
» python2 info2dir.py
» ls -la flag
drwxr-xr-x - pi  4 Aug 15:53 .git

» l1 flag/.git/
flag/.git
├── config
├── description
├── HEAD
├── hooks
├── index
├── info
├── objects
└── refs


» git -C flag log | head -5
commit f16174c1f5834c3833f75d6fbfd8252e5c5a7f64
Author: sui <hisui@protonmail.com>
Date:   Thu Aug 4 15:50:39 2022 +0700

    Remove flag.txt
```

### **Getting Flag**

Looking at the `.git`, we can see that the flag was being pushed once per commit.

```bash
» git show
commit f16174c1f5834c3833f75d6fbfd8252e5c5a7f64 (HEAD -> master)
Author: sui <hisui@protonmail.com>
Date:   Thu Aug 4 15:50:39 2022 +0700

    Remove flag.txt

diff --git a/flag.txt b/flag.txt
deleted file mode 100644
index 5c34318..0000000
--- a/flag.txt
+++ /dev/null
@@ -1 +0,0 @@
-}
```

Thus, the flag can be retrieved by using this simple script

```bash
» git log --pretty=format:%h | xargs -Iz bash -c 'git diff z | tac | grep -m1 -o .$' | tac | paste -sd ''

COMPFEST14{m4yhem_1n_d1sguise_huh_31408fca5d}
```

### **References**
- https://pkware.cachefly.net/webdocs/casestudies/APPNOTE.TXT
- https://abelcheung.github.io/rifiuti2/technical/
