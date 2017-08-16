folder('packages')
folder('packages/windows')

def scripts = ['win32_unstable_omp_mpi', 'win64_unstable_omp_mpi', 'win32_stable_omp_mpi', 'win64_stable_omp_mpi']

scripts.each { name ->
    pipelineJob("packages/windows/${name}") {
        triggers {
            githubPush()
        }

        logRotator(30)

        definition {
            cpsScm {
                scm {
                    git {
                        remote {
                            github('lammps/lammps-packages')
                            credentials('lammps-jenkins')
                        }

                        branches('master')

                        configure { gitScm ->
                            gitScm / 'extensions' << 'hudson.plugins.git.extensions.impl.PathRestriction' {
                              includedRegions("jenkins/${name}.groovy")
                              excludedRegions('.*')
                          }
                        }
                    }
                }
                scriptPath("jenkins/${name}.groovy")
            }
        }
    }
}
