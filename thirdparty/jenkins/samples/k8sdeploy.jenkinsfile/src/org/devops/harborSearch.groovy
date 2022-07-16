package org.devops
import groovy.json.JsonSlurper

def PrintMes(value,color){
	colors = ['red'   : "\033[40;31m >>>>>>>>>>>${value}<<<<<<<<<<< \033[0m",
			  'blue'  : "\033[47;34m ${value} \033[0m",
			  'green' : "[1;32m>>>>>>>>>>${value}>>>>>>>>>>[m",
			  'green1' : "\033[40;32m >>>>>>>>>>>${value}<<<<<<<<<<< \033[0m" ]
	ansiColor('xterm') {
		println(colors[color])
	}
}

def searchTag(harbor_host,harbor_auth,NS,Service,SpecificV) {
	response = httpRequest authentication: "${harbor_auth}",
				contentType: 'APPLICATION_JSON_UTF8',
				acceptType: 'APPLICATION_JSON_UTF8',
				responseHandle: 'LEAVE_OPEN',
				consoleLogResponseBody: false,
				url: "http://${harbor_host}/api/repositories/${NS}/${Service}/tags"
	def jsonSlurper = new JsonSlurper()
	def object = jsonSlurper.parseText(response.content)
	response.close()
	for (def subObj : object){
		if (subObj.name == SpecificV){
							PrintMes("find out the tag: "+ SpecificV,"green")
							return true
		}
	}
	error "do not find repository tagged ${SpecificV}"
				
}

