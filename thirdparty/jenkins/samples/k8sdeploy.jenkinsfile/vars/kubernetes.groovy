//封装HTTP请求
def HttpReq(reqType,reqUrl,reqBody,envType){
    if (envType == "prod"){
        string apiServer = 'https://10.0.0.1:6443'
    }else {
        string apiServer = 'https://10.0.0.2:6443'
    }
    withCredentials([string(credentialsId: "kubernetes-token-${envType}", variable: 'kubernetestoken')]) {
      result = httpRequest customHeaders: [[maskValue: true, name: 'Authorization', value: "Bearer ${kubernetestoken}"],
                                           [maskValue: false, name: 'Content-Type', value: 'application/yaml'], 
                                           [maskValue: false, name: 'Accept', value: 'application/yaml']], 
                httpMode: reqType, 
                validResponseCodes: '100:399,404,409',  // 100:399 accsess , 404 resource not found , 409 AlreadyExists
                consoleLogResponseBody: true,
                ignoreSslErrors: true, 
                requestBody: reqBody,
                url: "${apiServer}/${reqUrl}"
                //quiet: true
    }
    return result
}
//新建Deployment
def CreateDeployment(nameSpace,requestYamlBody,envType){
    apiUrl = "apis/apps/v1/namespaces/${nameSpace}/deployments/"
    response = HttpReq('POST',apiUrl,requestYamlBody,envType)
    println(response)
}

//删除deployment
def DeleteDeployment(nameSpace,objName,envType){
    apiUrl = "apis/apps/v1/namespaces/${nameSpace}/deployments/${objName}"
    response = HttpReq('DELETE',apiUrl,"",envType)
    println(response)
}

//更新Deployment
def UpdateDeployment(nameSpace,objName,requestYamlBody,envType){
    apiUrl = "apis/apps/v1/namespaces/${nameSpace}/deployments/${objName}"
    response = HttpReq('PUT',apiUrl,requestYamlBody,envType)
    println(response)
}

//获取Deployment
def GetDeployment(nameSpace,objName,envType){
    apiUrl = "apis/apps/v1/namespaces/${nameSpace}/deployments/${objName}"
    response = HttpReq('GET',apiUrl,'',envType)
    return response
}

//新建Statefulset
def CreateStatefulset(nameSpace,requestYamlBody,envType){
    apiUrl = "apis/apps/v1/namespaces/${nameSpace}/statefulsets/"
    response = HttpReq('POST',apiUrl,requestYamlBody,envType)
    println(response)
}

//删除Statefulset
def DeleteStatefulset(nameSpace,objName,envType){
    apiUrl = "apis/apps/v1/namespaces/${nameSpace}/statefulsets/${objName}"
    response = HttpReq('DELETE',apiUrl,"",envType)
    println(response)
}

//更新Statefulset
def UpdateStatefulset(nameSpace,objName,requestYamlBody,envType){
    apiUrl = "apis/apps/v1/namespaces/${nameSpace}/statefulsets/${objName}"
    response = HttpReq('PUT',apiUrl,requestYamlBody,envType)
    println(response)
}

//获取Statefulset
def GetStatefulset(nameSpace,objName,envType){
    apiUrl = "apis/apps/v1/namespaces/${nameSpace}/statefulsets/${objName}"
    response = HttpReq('GET',apiUrl,'',envType)
    return response
}

//新建 ingress
def CreateIngress(nameSpace,requestYamlBody,envType){
    apiUrl = "apis/extensions/v1beta1/namespaces/${nameSpace}/ingresses/"
    response = HttpReq('POST',apiUrl,requestYamlBody,envType)
    println(response)
}

//删除 ingress
def DeleteIngress(nameSpace,objName,envType){
    apiUrl = "apis/extensions/v1beta1/namespaces/${nameSpace}/ingresses/${objName}"
    response = HttpReq('DELETE',apiUrl,"",envType)
    println(response)
}

//更新 ingress
def UpdateIngress(nameSpace,objName,requestYamlBody,envType){
    apiUrl = "apis/extensions/v1beta1/namespaces/${nameSpace}/ingresses/${objName}"
    response = HttpReq('PUT',apiUrl,requestYamlBody,envType)
    println(response)
}

//获取 Ingress
def GetIngress(nameSpace,objName,envType){
    apiUrl = "apis/extensions/v1beta1/namespaces/${nameSpace}/ingresses/${objName}"
    response = HttpReq('GET',apiUrl,'',envType)
    return response
}

//新建Service
def CreateService(nameSpace,requestYamlBody,envType){
    apiUrl = "api/v1/namespaces/${nameSpace}/services/"
    response = HttpReq('POST',apiUrl,requestYamlBody,envType)
    println(response)
}

//删除 Service
def DeleteService(nameSpace,objName,envType){
    apiUrl = "api/v1/namespaces/${nameSpace}/services/${objName}"
    response = HttpReq('DELETE',apiUrl,"",envType)
    println(response)
}

//更新 Service
def UpdateService(nameSpace,objName,requestYamlBody,envType){
    apiUrl = "api/v1/namespaces/${nameSpace}/services/${objName}"
    response = HttpReq('PUT',apiUrl,requestYamlBody,envType)
    println(response)
}

//获取 Service
def GetService(nameSpace,objName,envType){
    apiUrl = "api/v1/namespaces/${nameSpace}/services/${objName}"
    response = HttpReq('GET',apiUrl,'',envType)
    return response
}


//新建 StorageClass
def CreateStorageClass(nameSpace,requestYamlBody,envType){
    apiUrl = "apis/storage.k8s.io/v1/storageclasses"
    response = HttpReq('POST',apiUrl,requestYamlBody,envType)
    println(response)
}

//删除 StorageClass
def DeleteStorageClass(nameSpace,objName,envType){
    apiUrl = "apis/storage.k8s.io/v1/storageclasses/${objName}"
    response = HttpReq('DELETE',apiUrl,"",envType)
    println(response)
}

//更新 StorageClass
def UpdateStorageClass(nameSpace,objName,requestYamlBody,envType){
    apiUrl = "apis/storage.k8s.io/v1/storageclasses/${objName}"
    response = HttpReq('PUT',apiUrl,requestYamlBody,envType)
    println(response)
}

//获取 StorageClass
def GetStorageClass(nameSpace,objName,envType){
    apiUrl = "apis/storage.k8s.io/v1/storageclasses/${objName}"
    response = HttpReq('GET',apiUrl,'',envType)
    return response
}

//新建 PVC
def CreatePVC(nameSpace,requestYamlBody,envType){
    apiUrl = "api/v1/namespaces/${nameSpace}/persistentvolumeclaims"
    response = HttpReq('POST',apiUrl,requestYamlBody,envType)
    println(response)
}

//删除 PVC
def DeletePVC(nameSpace,objName,envType){
    apiUrl = "api/v1/namespaces/${nameSpace}/persistentvolumeclaims/${objName}"
    response = HttpReq('DELETE',apiUrl,"",envType)
    println(response)
}

//更新 PVC
def UpdatePVC(nameSpace,objName,requestYamlBody,envType){
    apiUrl = "api/v1/namespaces/${nameSpace}/persistentvolumeclaims/${objName}"
    response = HttpReq('PUT',apiUrl,requestYamlBody,envType)
    println(response)
}

//获取 PVC
def GetPVC(nameSpace,objName,envType){
    apiUrl = "api/v1/namespaces/${nameSpace}/persistentvolumeclaims/${objName}"
    response = HttpReq('GET',apiUrl,'',envType)
    return response
}


//新建 poddisruptionbudgets
def CreatePDB(nameSpace,requestYamlBody,envType){
    apiUrl = "apis/policy/v1beta1/namespaces/${nameSpace}/poddisruptionbudgets"
    response = HttpReq('POST',apiUrl,requestYamlBody,envType)
    println(response)
}

//删除 poddisruptionbudgets
def DeletePDB(nameSpace,objName,envType){
    apiUrl = "apis/policy/v1beta1/namespaces/${nameSpace}/poddisruptionbudgets/${objName}"
    response = HttpReq('DELETE',apiUrl,"",envType)
    println(response)
}

//更新 poddisruptionbudgets
def UpdatePDB(nameSpace,objName,requestYamlBody,envType){
    apiUrl = "apis/policy/v1beta1/namespaces/${nameSpace}/poddisruptionbudgets/${objName}"
    response = HttpReq('PUT',apiUrl,requestYamlBody,envType)
    println(response)
}

//获取 poddisruptionbudgets
def GetPDB(nameSpace,objName,envType){
    apiUrl = "apis/policy/v1beta1/namespaces/${nameSpace}/poddisruptionbudgets/${objName}"
    response = HttpReq('GET',apiUrl,'',envType)
    return response
}

//新建 configmap
def CreateConfigmap(nameSpace,requestYamlBody,envType){
    apiUrl = "api/v1/namespaces/${nameSpace}/configmaps"
    response = HttpReq('POST',apiUrl,requestYamlBody,envType)
    println(response)
}

//删除 configmap
def DeleteConfigmap(nameSpace,objName,envType){
    apiUrl = "api/v1/namespaces/${nameSpace}/configmaps/${objName}"
    response = HttpReq('DELETE',apiUrl,"",envType)
    println(response)
}

//更新 configmap
def UpdateConfigmap(nameSpace,objName,requestYamlBody,envType){
    apiUrl = "api/v1/namespaces/${nameSpace}/configmaps/${objName}"
    response = HttpReq('PUT',apiUrl,requestYamlBody,envType)
    println(response)
}

//获取 configmap
def GetConfigmap(nameSpace,objName,envType){
    apiUrl = "api/v1/namespaces/${nameSpace}/configmaps/${objName}"
    response = HttpReq('GET',apiUrl,'',envType)
    return response
}

//新建 daemonset
def CreateDaemonset(nameSpace,requestYamlBody,envType){
    apiUrl = "apis/apps/v1/namespaces/${nameSpace}/daemonsets"
    response = HttpReq('POST',apiUrl,requestYamlBody,envType)
    println(response)
}

//删除 daemonset
def DeleteDaemonset(nameSpace,objName,envType){
    apiUrl = "apis/apps/v1/namespaces/${nameSpace}/daemonsets/${objName}"
    response = HttpReq('DELETE',apiUrl,"",envType)
    println(response)
}

//更新 daemonset
def UpdateDaemonset(nameSpace,objName,requestYamlBody,envType){
    apiUrl = "apis/apps/v1/namespaces/${nameSpace}/daemonsets/${objName}"
    response = HttpReq('PUT',apiUrl,requestYamlBody,envType)
    println(response)
}

//获取 daemonset
def GetDaemonset(nameSpace,objName,envType){
    apiUrl = "apis/apps/v1/namespaces/${nameSpace}/daemonsets/${objName}"
    response = HttpReq('GET',apiUrl,'',envType)
    return response
}
