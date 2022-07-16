package org.devops

/*
 95        kubectl set image deployment urm-user urm-user=172.24.101.218/ehome2/urm-user:20200318201129 --namespace=ehome2 --record=true
 */
def PrintMes(value,color){
	colors = ['red'   : "\033[40;31m >>>>>>>>>>>${value}<<<<<<<<<<< \033[0m",
			  'blue'  : "\033[47;34m ${value} \033[0m",
			  'green' : "[1;32m>>>>>>>>>>${value}>>>>>>>>>>[m",
			  'green1' : "\033[40;32m >>>>>>>>>>>${value}<<<<<<<<<<< \033[0m" ]
	ansiColor('xterm') {
		println(colors[color])
	}
}

def deploymentHistorySearch(tag,Service,NS) {
	status = sh returnStatus: true, encoding: 'utf-8', script: "kubectl rollout history -n ${NS} deployment/${Service}"
	if(status == 0) {
	    historyDetail =sh returnStdout: true, script: "kubectl rollout history -n ${NS} deployment/${Service}"
		historyDetail = historyDetail.trim().tokenize("\n")
		for (def line : historyDetail) {
			line = line.tokenize()
			if(line.size >= 7 && line.get(6).endsWith(tag)){
				PrintMes("find out the tag: ","green")
				PrintMes("tag: " + line.get(6),"blue")
				PrintMes("num: " + line.get(0),"blue")
				return line.get(0)
			}
		}
		error "the tag: ${tag} did not find. please pick another tag to roll back"
	}
	error "do not found deployment/${Service},please check the deployment/${Service} exists or not "
}

def deploymentSearch(Service,NS) {
	status = sh returnStatus: true, encoding: 'utf-8', script: "kubectl -n ${NS} get deployment/${Service} -o name"
	if(status == 0) {
		PrintMes("find deployment/${Service}","blue")
		return true
	} else {
		PrintMes("can not find deployment/${Service}","red")
		return false
	}
}


def serviceSearch(Service,NS) {
	status = sh returnStatus: true, encoding: 'utf-8', script: "kubectl -n ${NS} get svc/${Service} -o name"
	if(status == 0) {
		PrintMes("find svc/${Service}","blue")
		return true
	} else {
		PrintMes("can not find svc/${Service}","red")
		return false
	}
}