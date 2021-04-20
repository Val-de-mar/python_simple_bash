# simplified shell
It's simplified implementation of bash
already done:
	ls<path> — List directory contents. If path is not stated it will be ".".
	cd<path> — changes directory to <path>. 
	echo — Prints text to the terminal window.
	mkdir<path> — Create a directory.
	cp<input path><output path> — copies file from <input path> to <output path> if name's not stated it will be the same.
	mv<input path><output path> — moves file from <input path> to <output path> if name's not stated it will be the same.
	rm<filename> — removes file.
	pwd — Print working directory.
	rmdir<path> — removes directory.
	xargs - takes arguments from input stream and put them as arguments in the end of command
	cat - prints file content as text
	touch - creates empty file
	
also added processing of $(...), | and execution of executable files 
to exit use ^C
"-" - in <path> means previous directory.
"~" - in <path> means home directory.
