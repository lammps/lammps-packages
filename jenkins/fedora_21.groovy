def build_rpm(image_name) {
    def envImage = docker.image(image_name)

    docker.withRegistry('https://registry.hub.docker.com', 'docker-registry-login') {
        // ensure image is current
        envImage.pull()

        def workdir = pwd()

        // use workaround (see https://issues.jenkins-ci.org/browse/JENKINS-34276)
        docker.image(envImage.imageName()).inside {
            stage 'Prepare RPM build environment'

            //sh 'ccache -M 5G'

            sh '''
            rm -rf rpmbuild/RPMS
            mkdir -p rpmbuild/SPECS
            mkdir -p rpmbuild/SOURCES
            mkdir -p rpmbuild/RPMS
            mkdir -p rpmbuild/SRPMS
            mkdir -p rpmbuild/BUILD
            mkdir -p rpmbuild/BUILDROOT

            datestr=$(date +%Y%m%d)
            sed -e "/^Version/s/\\(Version:[         ]\\+\\)[0-9].*$/\\1${datestr}/" lammps-packages/rpm/lammps.spec > rpmbuild/SPECS/lammps.spec
            #sed -e "s/make/make \\%\\{\\?\\_smp\\_mflags\\}/" rpmbuild/SPECS/lammps.spec.tmp > ~/rpmbuild/SPECS/lammps.spec
            cp -pv lammps-packages/rpm/lammps.sh rpmbuild/SOURCES/
            cp -pv lammps-packages/rpm/lammps.csh rpmbuild/SOURCES/
            '''

            sh 'echo "%_topdir ' + workdir + '/rpmbuild" >> ~/.rpmmacros'
            sh 'echo "%_smp_mflags -j8" >> ~/.rpmmacros'

            stage 'Build docs'

            sh 'make -C doc -j 8 html'
            sh 'make -C doc pdf'


            stage 'Generate current source tarball'

            sh '''git archive -v --output=rpmbuild/SOURCES/lammps-current.tar --prefix=lammps-current/ HEAD README LICENSE \
                src lib python examples/{README,ASPHERE,KAPPA,MC,VISCOSITY,dipole,peri,hugoniostat,colloid,crack,friction,msst,obstacle,body,sputter,pour,ELASTIC,neb,ellipse,flow,meam,min,indent,deposit,micelle,shear,srd,dreiding,eim,prd,rigid,COUPLE,peptide,melt,comb,tad,reax,balance,snap,USER/{awpmd,misc,phonon,cg-cmm,fep}} \
                bench potentials tools/*.cpp tools/*.f tools/msi2lmp tools/xmgrace tools/createatoms tools/colvars'''
            sh "tar --transform 's,^,lammps-current/,' --append -f rpmbuild/SOURCES/lammps-current.tar doc/Manual.pdf doc/src/PDF"
            sh 'gzip -f -9 rpmbuild/SOURCES/lammps-current.tar'

            stage 'Build RPMs'
            sh 'rpmbuild --clean --rmsource --rmspec -bb rpmbuild/SPECS/lammps.spec'
            //sh 'ccache -s'
        }
    }
}

node {
    stage 'Checkout'
    git url: 'https://github.com/lammps/lammps.git', branch: 'lammps-icms'

    dir('lammps-packages') {
        git url: 'https://github.com/lammps/lammps-packages.git', credentialsId: 'lammps-jenkins', branch: 'rpm-build'
    }

    def workdir = pwd()

    //env.CCACHE_DIR=workdir + '/.ccache'

    build_rpm('rbberger/lammps-testing:fedora_21')

    stage 'Archive RPMs'
    archive includes:'rpmbuild/**/*.rpm'

    sh 'mkdir -p ${LAMMPS_DOWNLOAD_RPM_DIR}/fedora/21'
    sh 'find ${LAMMPS_DOWNLOAD_RPM_DIR}/fedora/21 -mtime +30 -exec rm {} \\;'
    sh 'cp -R rpmbuild/RPMS/x86_64 ${LAMMPS_DOWNLOAD_RPM_DIR}/fedora/21'

    step([$class: 'WarningsPublisher', canComputeNew: false, consoleParsers: [[parserName: 'GNU Make + GNU C Compiler (gcc)']], defaultEncoding: '', excludePattern: '', healthy: '', includePattern: '', messagesPattern: '', unHealthy: ''])
}
