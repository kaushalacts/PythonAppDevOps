pipeline {
    agent {
        label "ec2"
    }
    

    stages {
    stage("hello world"){
        steps{
            echo "hi jenkins"
        }
    }
        stage("Deployment on PROD ENV") {  //job1
            steps {
                sh "docker rm -f webos"
                sh "docker pull thehiddenboy143/gfgdevops20flask"
                sh "docker run -dit --name webos -p 80:80 thehiddenboy143/gfgdevops20flask"
                }
            }
    }
}
