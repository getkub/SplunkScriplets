// Adhoc git checkout without plugin

stage('Git checkout - Manual') {
    steps {
        script {
            def config = [
                'githubUser': 'myuser'?: "defaultUser",
                'repo': 'my-repo-custom',
                'githubToken': 'my_pat'
            ]

            withCredentials([string(credentialsId: config.githubToken, variable: 'gitToken')]) {
                sh 'git clone https://'+config.githubUser+':'+gitToken+'@github.com/my-org/'+config.repo+'.git'
            }
        }
    }
}