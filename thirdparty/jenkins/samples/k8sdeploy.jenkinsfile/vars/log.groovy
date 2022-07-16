def warning(value){
	//purple
	ansiColor('xterm') {
		println("\033[35m WARNING: ${value} \033[0m")
	}
}

def error(value){
	//red
	ansiColor('xterm') {
		println("\033[31m ERROR:  ${value} \033[0m")
	}
}

def info(value){
	//blue
	ansiColor('xterm') {
		println("\033[34m INFO: ${value} \033[0m")
	}
}

def debug(value){
	//green
	ansiColor('xterm') {
		println("\033[32m DEBUG: ${value} \033[0m")
	}
}