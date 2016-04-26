from cryptography.fernet import Fernet
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
    LIBPATH = [
        '$INSTALL_DIR',
    ],

    # Generate a secret key for symmetric encryptino
    SECRET_KEY = Fernet.generate_key(),
)

# Add tools to base environment
base_env.Tool('compactor')
base_env.Tool('resource_serializer')

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
    ],
    LINKFLAGS = [
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
        # Create new base environment for Linux build systems
        build_env = env.Clone()
        build_env.Append(
            LINKFLAGS = [
                '-static',
                '-static-libgcc',
                '-static-libstdc++',
            ],
        )
            
        # Create Windows build environment
        win_env = build_env.Clone(
            OS = 'windows',
            MINGW_PREFIX = 'x86_64-w64-mingw32-',
            CC = '${MINGW_PREFIX}gcc',
            CXX = '${MINGW_PREFIX}g++',
            LD = '${MINGW_PREFIX}ld',
            AR = '${MINGW_PREFIX}ar',
            PROGSUFFIX = '.exe',
        )
        # Add Windows build environment to build environment list
        build_envs.append(win_env)

        # Create Linux build environment
        lnx_env = build_env.Clone(OS = platform)
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
