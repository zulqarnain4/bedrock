#!groovy

// define deployment & integration test targets
def allRegions = [
    [deis: 'usw', name: 'us-west'],
    [deis: 'euw', name: 'eu-west'],
]
def deployAndTestProps = [
    master: [
        regions: allRegions,
        apps: ['bedrock-dev'],
        props: 'per_push',
    ],
    prod: [
        regions: allRegions,
        apps: ['bedrock-stage', 'bedrock-prod'],
        props: 'per_tag',
    ],
    'deploy-via-jenkinsfile': [
        regions: allRegions,
        apps: ['bedrock-jenkinsfile-test'],
        props: 'per_push',
    ],
]
def propFiles = [
    baseDir: 'docker/jenkins/properties/integration_tests',
    fileExt: '.properties',
]

/** Send a notice to #www on irc.mozilla.org with the build result
 *
 * @param stage step of build/deploy
 * @param result outcome of build (will be uppercased)
*/
def ircNotification(stage, status) {
    sh "bin/irc-notify.sh --stage '${stage}' --status '${status}'"
}

def buildDockerImage(Map kwargs) {
    def update = kwargs.update ? 'true' : 'false'
    def repo = kwargs.dockerRepo ?: 'mozorg'
    def script = kwargs.script ?: 'build_image.sh'
    def environs = ["UPDATE_DOCKER_IMAGES=${update}",
                    "DOCKERFILE=${kwargs.dockerfile}",
                    "DOCKER_REPOSITORY=${repo}/${kwargs.dockerfile}"]
    if (kwargs.fromDockerfile) {
        environs << "FROM_DOCKER_REPOSITORY=${repo}/${kwargs.fromDockerfile}"
    }
    withEnv(environs) {
        sh 'env'
        sh "docker/jenkins/${script}"
    }
}

def pushDockerhub(from_repo, to_repo='') {
    to_repo = to_repo ?: from_repo
    withCredentials([[$class: 'StringBinding',
                      credentialsId: 'DOCKER_PASSWORD',
                      variable: 'DOCKER_PASSWORD']]) {
        withEnv(['DOCKER_USERNAME=mozjenkins',
                 "FROM_DOCKER_REPOSITORY=${from_repo}",
                 "DOCKER_REPOSITORY=${to_repo}"]) {
            retry(2) {
                sh 'docker/jenkins/push2dockerhub.sh'
            }
        }
    }
}

def pushPrivateReg(region) {
    def registryPorts = [usw: '5001', euw: '5000']
    retry(3) {
        // TODO Fix DEIS_APPS before merge
        // DEIS_APPS=bedrock-dev,bedrock-stage,bedrock-prod
        withEnv(['FROM_DOCKER_REPOSITORY=mozorg/bedrock_l10n',
                 "PRIVATE_REGISTRIES=localhost:${registryPorts[region]}",
                 'DEIS_APPS=bedrock-jenkinsfile-test']) {
            sh 'docker/jenkins/push2privateregistries.sh'
        }
    }
}

stage ('Checkout') {
    node {
        checkout scm
        sh 'git submodule sync'
        sh 'git submodule update --init --recursive'
        env.GIT_COMMIT = sh([returnStdout: true, script: 'git rev-parse HEAD']).trim()
        stash name: 'scripts', includes: 'bin/,docker/'
        stash name: 'tests', includes: 'tests/,requirements/'
        stash 'workspace'
    }
}

// !!!!!!! ONLY FOR TESTING. REMOVE BEFORE MERGE !!!!!!!
if ( env.BRANCH_NAME == 'deploy-via-jenkinsfile') {
    stage ('Build Base') {
        node {
            unstash 'workspace'
            ircNotification('Test & Deploy', 'starting')
            try {
                buildDockerImage(dockerfile: 'bedrock_base', update: true)
            } catch(err) {
                ircNotification('Base Build', 'failure')
                throw err
            }
        }
    }

    stage ('Build Code') {
        parallel build: {
            node {
                unstash 'workspace'
                try {
                    buildDockerImage(dockerfile: 'bedrock_code', fromDockerfile: 'bedrock_base')
                } catch(err) {
                    ircNotification('Code Build', 'failure')
                    throw err
                }
            }
        },
        push: {
            node {
                unstash 'scripts'
                try {
                    pushDockerhub('mozorg/bedrock_base')
                } catch(err) {
                    ircNotification('Dockerhub Base Push', 'warning')
                }
            }
        }
    }

    stage ('Unit Test') {
        parallel build: {
            node {
                unstash 'scripts'
                try {
                    withEnv(['DOCKER_REPOSITORY=mozorg/bedrock_code']) {
                        sh 'docker/jenkins/run_tests.sh'
                    }
                } catch(err) {
                    ircNotification('Unit Test Code Image', 'failure')
                    throw err
                }
            }
        },
        push: {
            node {
                unstash 'scripts'
                try {
                    pushDockerhub('mozorg/bedrock_code')
                } catch(err) {
                    ircNotification('Dockerhub Code Push', 'warning')
                }
            }
        }
    }

    stage ('Build L10n') {
        node {
            unstash 'scripts'
            try {
                buildDockerImage(dockerfile: 'bedrock_l10n', fromDockerfile: 'bedrock_code', script: 'include_l10n.sh')
            } catch(err) {
                ircNotification('L10n Build', 'failure')
                throw err
            }
            ircNotification('Docker Builds', 'complete')
        }
    }

    stage ('Push Images') {
        // push images to docker hub and internal registries
        parallel dockerhub: {
            node {
                unstash 'scripts'
                try {
                    pushDockerhub('mozorg/bedrock_l10n', 'mozorg/bedrock')
                } catch(err) {
                    ircNotification('Dockerhub Push Failed', 'warning')
                }
            }
        },
        registry_usw: {
            node {
                unstash 'scripts'
                try {
                    pushPrivateReg('usw')
                } catch(err) {
                    ircNotification('US-West Registry Push', 'failure')
                    throw err
                }
            }
        },
        registry_euw: {
            node {
                unstash 'scripts'
                try {
                    pushPrivateReg('euw')
                } catch(err) {
                    ircNotification('EU-West Registry Push', 'failure')
                    throw err
                }
            }
        }
        node {
            unstash 'scripts'
            ircNotification('Docker Image Pushes', 'complete')
        }
    }

    def deployProps = deployAndTestProps[env.BRANCH_NAME]
    for (appname in deployProps.apps) {
        for (region in deployProps.regions) {
            stage ("Deploy ${appname}-${region.name}") {
                node {
                    unstash 'scripts'
                    withEnv(["DEIS_PROFILE=${region.deis}",
                             "DOCKER_REPOSITORY=${appname}",
                             "DEIS_APPLICATION=${appname}"]) {
                        retry(3) {
                            sh 'docker/jenkins/push2deis.sh'
                        }
                    }
                }
            }
            stage ("Test ${appname}-${region.name}") {
                def allTests = [:]
                node {
                    unstash 'scripts'
                    def files = findFiles(glob: "${propFiles.baseDir}/${deployProps.props}/*${propFiles.fileExt}")
                    for (file in files) {
                        allTests[]
                        echo "file name: ${file.name}"
                        echo "file path: ${file.path}"
                        echo "file dir: ${file.directory}"
                    }
                }
            }
        }
    }
}

if ( env.BRANCH_NAME == 'master' ) {
    node {
        ircNotification('Dev Deploy', 'starting')
        build 'bedrock_base_image'
    }
}
else if ( env.BRANCH_NAME == 'prod') {
    node {
        ircNotification('Stage & Prod Deploys', 'starting')
        build 'bedrock_base_image'
    }
}
else if ( env.BRANCH_NAME ==~ /^demo__[\w-]+$/ ) {
    node {
        ircNotification('Demo Deploy', 'starting')
        try {
            stage ('build') {
                sh 'make clean'
                sh 'make sync-all'
                sh 'echo "ENV GIT_SHA ${GIT_COMMIT}" >> docker/dockerfiles/bedrock_dev_final'
                sh 'echo "RUN echo ${GIT_COMMIT} > static/revision.txt" >> docker/dockerfiles/bedrock_dev_final'
                sh 'make build-final'
            }
        } catch(err) {
            ircNotification('Demo Build', 'failure')
            throw err
        }

        try {
            stage ('deploy') {
                withCredentials([[$class: 'StringBinding',
                                  credentialsId: 'SENTRY_DEMO_DSN',
                                  variable: 'SENTRY_DEMO_DSN']]) {
                    withEnv(['DEIS_PROFILE=usw', 'PRIVATE_REGISTRY=localhost:5001']) {
                        sh './docker/jenkins/demo_deploy.sh'
                    }
                }
            }
        } catch(err) {
            ircNotification('Demo Deploy', 'failure')
            throw err
        }
    }
}
else {
    echo "Doing nothing for ${env.BRANCH_NAME}"
}
