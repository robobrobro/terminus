from SCons.Errors import StopError
import copy, os, platform

# Base environment
env = Environment(
    BUILD_ROOT = '#build',
    BUILD_DIR = '$BUILD_ROOT/$OS/$MODE',
    INSTALL_ROOT = '$BUILD_ROOT/bin',
    INSTALL_DIR = '$INSTALL_DIR/$OS/$MODE',
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

# Set base environments
base_envs = [
    dbg_env,
    rel_env,
]

# Initialize environments in which to build
build_envs = copy.copy(base_envs)

# Get platform of the build system
platform = platform.system().lower()

# Create and add new build environments based on the build system's platform
# Linux systems cross-compile for Windows as well as native-compile for Linux
# Mac (Darwin) systems native-compile for Darwin
if platform == 'linux':
    # Create build environment for every base build environment
    for env in base_envs:
        # Create Windows build environment
        win_env = env.Clone(OS = 'windows')
        # TODO add Windows-specific settings
        # Add Windows build environment to build environment list
        build_envs.append(win_env)

        # Create Linux build environment
        lnx_env = env.Clone(OS = platform)
        # TODO add Linux-specific settings
        # Add Linux build environment to build environment list
        build_envs.append(lnx_env)
elif platform is 'darwin':
    # Create build environment for every base build environment
    for env in base_envs:
        # Create Darwin build environment
        darwin_env = env.Clone(OS = darwin)
        # TODO add Darwin-specific settings
        # Add Darwin build environment to build environment list
        build_envs.append(darwin_env)
else:
    raise StopError('Unknown build system platform: {}'.format(platform))

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
