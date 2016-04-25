from SCons.Errors import StopError
import copy, os, platform

# Base environment
base_env = Environment(
    BUILD_ROOT = '#build',
    BUILD_DIR = '$BUILD_ROOT/$OS/$MODE',
    INSTALL_ROOT = '$BUILD_ROOT/bin',
    INSTALL_DIR = '$INSTALL_ROOT/$OS/$MODE',

    CCFLAGS = [
        '-std=c++11',
    ],
    LINKFLAGS = [
        '-static-libgcc',
        '-static-libstdc++',
    ],
    LIBPATH = [
        '$INSTALL_DIR',
    ],
)

# Build debug and release environments
dbg_env = base_env.Clone(MODE = 'debug')
dbg_env.Append(
    CCFLAGS = [
        '-g',
        '-O0',
    ],
)

rel_env = base_env.Clone(MODE = 'release')
rel_env.Append(
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

# Get platform of the build system
platform = ARGUMENTS.get('platform', platform.system()).lower()

# Platform map
PLATFORMS = {
    'linux': ['linux', 'lnx'],
    'mac': ['mac', 'darwin', 'osx'],
}

# Create and add new build environments based on the build system's platform
build_envs = []

# Linux systems cross-compile for Windows as well as native-compile for Linux
# Mac (Darwin) systems native-compile for Darwin
if platform in PLATFORMS['linux']:
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
elif platform in PLATFORMS['mac']:
    # Create build environment for every base build environment
    for env in base_envs:
        # Create Darwin build environment
        darwin_env = env.Clone(OS = platform)
        # TODO add Darwin-specific settings
        # Add Darwin build environment to build environment list
        build_envs.append(darwin_env)
else:
    platforms = ', '.join(sorted([p for l in PLATFORMS.itervalues() for p in l]))
    msg = 'Invalid platform: {} (choices: {}).'.format(platform, platforms)
    raise StopError(msg)

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
