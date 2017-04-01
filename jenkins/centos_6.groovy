node {
    stage 'Checkout'
    git url: 'https://github.com/lammps/lammps.git', branch: 'lammps-icms'

    dir('lammps-packages') {
        git url: 'https://github.com/lammps/lammps-packages.git', credentialsId: 'lammps-jenkins', branch: 'rpm-build'
    }

    def common = load 'lammps-packages/jenkins/common.groovy'

    def workdir = pwd()

    //env.CCACHE_DIR=workdir + '/.ccache'

    common.build_rpm('rbberger/lammps-testing:centos_6')

    stage 'Archive RPMs'
    archive includes:'rpmbuild/**/*.rpm'

    sh 'mkdir -p ${LAMMPS_DOWNLOAD_RPM_DIR}/centos/6'
    sh 'find ${LAMMPS_DOWNLOAD_RPM_DIR}/centos/6 -mtime +30 -exec rm {} \\;'
    sh 'cp -R rpmbuild/RPMS/x86_64 ${LAMMPS_DOWNLOAD_RPM_DIR}/centos/6'

    step([$class: 'WarningsPublisher', canComputeNew: false, consoleParsers: [[parserName: 'GNU Make + GNU C Compiler (gcc)']], defaultEncoding: '', excludePattern: '', healthy: '', includePattern: '', messagesPattern: '', unHealthy: ''])
}
