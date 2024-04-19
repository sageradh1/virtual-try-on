pipeline {
	agent any
    
    environment {
        APP_VERSION = '0.0.1'
    }

    stages {

        stage('Stage 1 - Cloning Source Repository') {
            steps {
                sh script:'''
                    #!/bin/bash
                    echo 'Cloning began......'
                '''
                checkout scm
                
            }
        }

        stage('Stage 2 - Removing past containers') {
            steps {
                catchError(buildResult: 'SUCCESS', stageResult: 'FAILURE') {
                    sh script:'''
                        #!/bin/bash
                        echo 'Repo removal began......'
                        cd /var/lib/jenkins/workspace/vto
                        workfolder=$(pwd)
                        
                        docker compose stop
                        docker compose rm -f

                        '''  
                }
            }
        }

        stage('Stage 3 - Building and starting new containers') {
            steps {
                sh script:'''
                    #!/bin/bash
                    echo 'Building and restarting......'
                    
                    cd /var/lib/jenkins/workspace/vto
                    workfolder=$(pwd)

                    cd ../../
                    sudo chmod -R 755 workspace
                    cd $workfolder
                    docker compose up --build
                    '''  
            }
        }

    
    }

}