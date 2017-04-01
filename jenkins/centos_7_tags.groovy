node {
    stage 'Checkout'

    checkout([$class: 'GitSCM', branches: [[name: '**/tags/*']], doGenerateSubmoduleConfigurations: false, extensions: [[$class: 'BuildChooserSetting', buildChooser: [$class: 'AncestryBuildChooser', ancestorCommitSha1: '', maximumAgeInDays: 30]]], submoduleCfg: [], userRemoteConfigs: [[credentialsId: 'lammps-jenkins', refspec: '+refs/tags/*:refs/remotes/origin/tags/*', url: 'https://github.com/lammps/lammps.git']]])

    dir('lammps-packages') {
        git url: 'https://github.com/lammps/lammps-packages.git', credentialsId: 'lammps-jenkins', branch: 'rpm-build'
    }

    def common = load 'lammps-packages/jenkins/common.groovy'

    def workdir = pwd()

    //env.CCACHE_DIR=workdir + '/.ccache'

    common.build_rpm('rbberger/lammps-testing:centos_7', 'release')

    stage 'Archive RPMs'
    archiveArtifacts artifacts: 'rpmbuild/**/*.rpm', onlyIfSuccessful: true

    sh 'mkdir -p ${LAMMPS_DOWNLOAD_RPM_DIR}/stable/centos/7'
    sh 'find ${LAMMPS_DOWNLOAD_RPM_DIR}/stable/centos/7 -mtime +30 -exec rm {} \\;'
    sh 'cp -R rpmbuild/RPMS/x86_64 ${LAMMPS_DOWNLOAD_RPM_DIR}/stable/centos/7'

    step([$class: 'WarningsPublisher', canComputeNew: false, consoleParsers: [[parserName: 'GNU Make + GNU C Compiler (gcc)']], defaultEncoding: '', excludePattern: '', healthy: '', includePattern: '', messagesPattern: '', unHealthy: ''])
}
