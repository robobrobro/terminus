import os, platform

# Base environment
env = Environment(
    BUILD_ROOT = '#build',
    BUILD_DIR = '$BUILD_ROOT/$OS/$MODE',
    INSTALL_ROOT = '$BUILD_ROOT/bin',
    INSTALL_DIR = '$INSTALL_DIR/$OS/$MODE',

    OS = platform.system().lower(),
)

# Build debug and release environments
dbg_env = Environment(
    MODE = 'debug',
    CCFLAGS = [
        '-g',
        '-O0',
    ],
)

rel_env = Environment(
    MODE = 'release',
    CCFLAGS = [
        '-O3',
        '-s',
    ],
)

# Set environments in which to build
build_envs = [
    dbg_env,
    rel_env,
]

# Build every subdir that has an SConscript in every build environment
for subdir in filter(os.path.isdir, os.listdir(Dir('.').srcnode().abspath)):
    if 'SConscript' in os.listdir(subdir):
        for env in build_envs:
            objs = SConscript(
                dirs=subdir,
                exports=dict(env=env.Clone()),
                variant_dir=env.subst('$BUILD_DIR/') + subdir,
                duplicate=False,
            )
    
            env.Install('$INSTALL_DIR', objs)
