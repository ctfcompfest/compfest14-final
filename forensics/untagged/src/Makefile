all:
	git init flag
	cat flag.txt | fold -w1 | xargs -Iz bash -c 'echo z > flag/flag.txt; git -C flag add .; git -C flag commit -m "Add flag.txt"' || true
	rm flag/flag.txt
	git -C flag add .
	git -C flag commit -m "Remove flag.txt"
	rm -rf flag/.git/logs
	rm -rf flag/.git/COMMIT_EDITMSG
	./rem flag
	7z a -pcycleleergreycactus pre_untagged.zip Recycler
	python2 mod.py pre_untagged.zip untagged.zip

test:
	-@python3 rebuild_ch.py untagged.zip untagged_fixed.zip 
	-@7z x -pcycleleergreycactus untagged_fixed.zip
	-@python2 info2dir.py
	-@git -C flag log --oneline | tac | cut -d' ' -f1 | xargs -Iz bash -c 'git -C flag diff z | tail -1 | cut -c2- ' | paste -sd ''

clean:
	-@rm -rf flag
	-@rm -rf untagged_fixed.zip
	-@rm -rf pre_untagged.zip
	-@rm -rf Recycler
