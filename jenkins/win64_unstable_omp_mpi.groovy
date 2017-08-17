node {
    def arch = 64
    def lammps_branch = 'unstable'

    stage('Checkout') {
        dir('lammps') {
            git branch: lammps_branch, credentialsId: 'lammps-jenkins', url: 'https://github.com/lammps/lammps.git'
        }
        
        dir('lammps-packages') {
            git branch: 'master', credentialsId: 'lammps-jenkins', url: 'https://github.com/lammps/lammps-packages.git'
        }
    }

    def mingw_cross = load 'lammps-packages/jenkins/mingw_cross.groovy'

    mingw_cross.build_installer('-b ' + arch + ' -r ' + lammps_branch + ' -t omp -p mpi -j 8')

    stage('Publish') {
        archiveArtifacts artifacts: '*.exe', fingerprint: true, onlyIfSuccessful: true
        sh 'mkdir -p ${LAMMPS_DOWNLOAD_WINDOWS_DIR}/' + lammps_branch
        sh 'find ${LAMMPS_DOWNLOAD_WINDOWS_DIR}/' + lammps_branch + ' -mtime +30 -exec rm {} \\;'
        sh 'cp *.exe ${LAMMPS_DOWNLOAD_WINDOWS_DIR}/' + lammps_branch + '/'
    }
}
