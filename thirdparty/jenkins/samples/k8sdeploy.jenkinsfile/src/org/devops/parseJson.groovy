package org.devops
import groovy.json.JsonSlurper 

def parser(jsonobj) {
	def jsonSlurper = new JsonSlurper()
	def object = jsonSlurper.parseText(jsonobj)
	return object
}