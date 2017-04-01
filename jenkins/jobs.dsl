folder('rpms/daily')
folder('rpms/tags')

def scripts = ['centos_6', 'centos_7', 'fedora_21', 'fedora_22', 'fedora_23', 'fedora_24', 'fedora_25', 'opensuse_13.2', 'opensuse_42.1', 'opensuse_42.2']

scripts.each { name ->
    pipelineJob("rpms/daily/${name}") {
        triggers {
            cron('@midnight')
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

                        branches('rpm-build')

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

def scripts2 = ['centos_7']

scripts2.each { name ->
    pipelineJob("rpms/tags/${name}") {
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

                        branches('rpm-build')

                        configure { gitScm ->
                            gitScm / 'extensions' << 'hudson.plugins.git.extensions.impl.PathRestriction' {
                              includedRegions("jenkins/${name}_tags.groovy")
                              excludedRegions('.*')
                          }
                        }
                    }
                }
                scriptPath("jenkins/${name}_tags.groovy")
            }
        }
    }
}
