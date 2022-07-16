package org.devops


def PrintMes(value,color){
	colors = ['red'   : "\033[40;31m >>>>>>>>>>>${value}<<<<<<<<<<< \033[0m",
			  'blue'  : "\033[47;34m ${value} \033[0m",
			  'green' : "[1;32m>>>>>>>>>>${value}>>>>>>>>>>[m",
			  'green1' : "\033[40;32m >>>>>>>>>>>${value}<<<<<<<<<<< \033[0m" ]
	ansiColor('xterm') {
		println(colors[color])
	}
}

def checkPodStatus(String Service,String NS) {
	status =sh returnStatus: true, script: "kubectl rollout status --timeout=300s deployment/${Service} -n ${NS}"
	if (status == 0) {
		    ser_status =sh returnStdout: true, script: "kubectl rollout status --timeout=300s deployment/${Service} -n ${NS}"
			ser_status = ser_status.trim()
			if (ser_status.endsWith("successfully rolled out")){
				println(ser_status)
				podInfo= sh returnStdout:true,script: "kubectl -n ${NS} get deployment/${Service} -o wide --no-headers"
				if (podInfo) {
					podInfo = podInfo.trim().tokenize()
					PrintMes("deployment infomation:","blue")
					PrintMes("Service: "+ podInfo.get(0),"blue")
					PrintMes("ready num: "+ podInfo.get(1),"blue")
					PrintMes("AVAILABLE num: "+ podInfo.get(3),"blue")
					PrintMes("image name: "+ podInfo.get(6),"blue")
				}

			}else {
				println(ser_status)
				podInfo= sh returnStdout:true,script: "kubectl -n ${NS} get deployment/${Service} -o wide --no-headers"
				if (podInfo) {

					podInfo = podInfo.trim().tokenize()
					PrintMes("deployment infomation:","blue")
					PrintMes("Service: "+ podInfo.get(0),"blue")
					PrintMes("ready num: "+ podInfo.get(1),"blue")
					PrintMes("AVAILABLE num: "+ podInfo.get(3),"blue")
					PrintMes("image name: "+ podInfo.get(6),"blue")
				}
				error "rollout failure"
			}
	}else {
		sh returnStatus: true, script: "kubectl -n ${NS} get deployment/${Service} -o wide"
		error "can not find deployment server: ${Service}, please check the project create first or not"
	}
}

def checkSvcStatus(Service,NS,Port) {
	status = sh returnStatus: true, encoding: 'utf-8', script: "kubectl -n ${NS} get svc/${Service} -o name"
	if (status == 0) {
		ser_status =sh returnStdout: true, script: "kubectl -n ${NS} get svc/${Service} --no-headers"
		ser_status = ser_status.trim()
		println('svc health check')
		column =ser_status.tokenize()
		if (Port instanceof java.util.ArrayList) {
			ports = column.get(4).tokenize(',')
			for(def port: ports) {
				port = port.tokenize('/')
				port = port.get(0).tokenize(':')
				println(port)
				if (Port.contains(port.get(1))) {
					println("PORT linsten: ${port.get(1)}")
				} else {
					error "find a non list port listen in the service: ${port.get(1)}"
				}
			}
			PrintMes("service: ${column.get(0)}","blue")
			PrintMes("type: ${column.get(1)}","blue")
			PrintMes("CLUSTER-IP : ${column.get(2)}","blue")
			PrintMes("EXTERNAL-IP: ${column.get(3)}","blue")
			PrintMes("AGE: ${column.get(5)}","blue")
			return true
			
		} else {
			port = column.get(4).tokenize('/').get(0)
			if (port.endsWith(Port)) {
				PrintMes("PORT linsten: ${port}","blue")
				PrintMes("service: ${column.get(0)}","blue")
				PrintMes("type: ${column.get(1)}","blue")
				PrintMes("CLUSTER-IP : ${column.get(2)}","blue")
				PrintMes("EXTERNAL-IP: ${column.get(3)}","blue")
				PrintMes("AGE: ${column.get(5)}","blue")
				return true
			}else {
				error "port listen on error port: ${port}"
			}
		}
		
		error "can not find svc server: ${Service} listen on ${Port},please check the project create first or not"

	}else {
		error "can not find svc server: ${Service} listen on ${Port},please check the project create first or not"
	}
}
