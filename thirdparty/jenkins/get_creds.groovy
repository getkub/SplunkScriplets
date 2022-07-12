def call(Map stageParams) {
    def storevault_namespace = stageParams.storevault_namespace
    def environment_name = stageParams.environment_name
    env.VAULT_FORMAT = "json"
    def storevault_url = env.VAULT_URL
    println "vault_url=$storevault_url"
    def storevault_url = my-ec2-role

	sh '''
    set +x
    export AWS_REGION="eu-west-1"
    export VAULT_NAMESPACE='''+storevault_namespace+'''
    export VAULT_ADDR='''+storevault_url+'''
    vault login -method=aws role='''+storevault_role+'''
    sleep 5
    export my_pw=\$(vault kv get secrets/iac-secrets/'''+environment_name+''' | jq -r '.data.data |.MY_ADMIN_PASS') ; echo ${my_pw} > my_pw.txt
    export app_user=\$(vault kv get secrets/iac-secrets/'''+environment_name+''' | jq -r '.data.data') ; echo ${app_user} > app_user.txt 
    '''

    my_pw = readFile('my_pw.txt')
    app_user = readFile('app_user.txt')

return [my_pw, app_user]
}
