def build_installer(options) {
    stage('Prepare Environment') {
        def envImage = docker.image('rbberger/lammps-testing:fedora_26')

        docker.withRegistry('https://registry.hub.docker.com', 'docker-registry-login') {
            // ensure image is current
            envImage.pull()

            docker.image(envImage.imageName()).inside {
                stage('Build') {
                    sh 'python lammps-packages/mingw-cross/build-win-on-linux.py ' + options
                }
            }
        }
    }
}
return this
