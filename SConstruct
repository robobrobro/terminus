from SCons.Errors import StopError
import binascii, copy, os, platform

# Platform map
PLATFORMS = {
    'linux': ['linux', 'lnx'],
    'mac': ['mac', 'darwin', 'osx'],
}

platforms = sorted([p for l in PLATFORMS.itervalues() for p in l])

# Get platform of the build system
platform = ARGUMENTS.get('platform', platform.system()).lower()

# Verify platform is known
if platform not in platforms:
    msg = 'Invalid platform: {} (choices: {}).'.format(platform, ', '.join(platforms))
    raise StopError(msg)

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

    # Get platform of the build system
    PLATFORM = [p for p in PLATFORMS if platform in PLATFORMS[p]][0],

    # Get path to the SConstruct
    SCONSTRUCT = os.path.join(Dir('.').srcnode().abspath, 'SConstruct'),

    # Generate a secret key for symmetric encryption
    SECRET_KEY = binascii.hexlify(os.urandom(4096)),
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
)

# Set base environments
base_envs = [
    dbg_env,
    rel_env,
]

# Create and add new build environments based on the build system's platform
build_envs = []

# Linux systems cross-compile for Windows as well as native-compile for Linux
# Mac (Darwin) systems native-compile for Darwin
if platform in PLATFORMS['linux']:
    # Create build environment for every base build environment
    for env in base_envs:
        # Create new base environment for Linux build systems
        build_env = env.Clone(
            CC = '${MINGW_PREFIX}gcc',
            CXX = '${MINGW_PREFIX}g++',
            LD = '${MINGW_PREFIX}ld',
            AR = '${MINGW_PREFIX}ar',
        )
        build_env.Append(
            LINKFLAGS = [
                '-static',
                '-static-libgcc',
                '-static-libstdc++',
                '-s',
            ],
        )

        # Create Windows build environment
        win_env = build_env.Clone(
            OS = 'windows',
            MINGW_PREFIX = 'x86_64-w64-mingw32-',
            PROGSUFFIX = '.exe',
        )
        win_env.Append(LIBPATH = '/usr/lib/x86_64-w64-mingw32')
        # Add Windows build environment to build environment list
        build_envs.append(win_env)

        # Create Linux build environment
        lnx_env = build_env.Clone(
            OS = platform,
            MINGW_PREFIX = 'x86_64-linux-gnu-',
        )
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
